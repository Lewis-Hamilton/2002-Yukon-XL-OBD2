import logging
import time
from datetime import datetime

from yukon_watcher.args import parser
from yukon_watcher.calculations.gear_calc import estimate_gear
from yukon_watcher.calculations.idle_calc import idle_ready
from yukon_watcher.obd_utils import obd_state

args = parser.parse_args()
logger = logging.getLogger(__name__)

# Update intervals per priority, in seconds
PRIORITY_INTERVALS = {"fast": 0.75, "medium": 2.5, "slow": 10.0}
CSV_WRITE_INTERVAL = 1.0
LOOP_SLEEP = 0.05  # Small sleep to prevent CPU hammering
ERROR_BACKOFF = 1.0  # Pause after an unexpected error before retrying


def _poll_due_sensors(all_data, last_update_times, current_time):
    """Queries every sensor that's due for an update. A single sensor
    failing (dropped OBD connection, bad reading, Pi read error, etc.)
    is skipped rather than aborting the whole cycle -- this is what lets
    Pi-only data keep flowing even when OBD is absent or misbehaving.
    """
    updates = {}
    for data in all_data:
        interval = PRIORITY_INTERVALS.get(data.priority)
        if interval is None or args.manual_testing:
            continue
        if current_time - last_update_times[data.name] < interval:
            continue

        try:
            value = data.response
        except Exception as e:  # noqa: BLE001
            logger.debug(f"Skipping {data.name} this cycle: {e}")
            continue

        if value is not None:
            updates[data.name] = value
            last_update_times[data.name] = current_time

    return updates


def _reset_obd_fields(all_data, data_store):
    """No live OBD connection -- hold every OBD-sourced value at its
    default instead of displaying whatever was last read before the car
    went quiet. Pi-only fields (AddedData without a `cmd`, e.g. CPU/RAM/
    temp) are left alone since they're independent of OBD.
    """
    for data in all_data:
        if hasattr(data, "cmd"):  # ObdData, not Pi-sourced
            data_store[data.name] = 0
    data_store["Estimated Gear"] = "---"
    data_store["Idle Indicator"] = None


def _update_calculated_fields(local_updates, data_store):
    """Estimated gear / idle status are derived from RPM, Speed, and
    Engine Load. Only called while actually connected -- see
    _reset_obd_fields for the disconnected case.
    """
    current_rpm = local_updates.get("RPM", data_store.get("RPM", 0))
    current_speed = local_updates.get("Speed", data_store.get("Speed", 0))
    current_load = local_updates.get("Engine Load", data_store.get("Engine Load", 0))

    if current_rpm is not None and current_speed is not None:
        data_store["Estimated Gear"] = estimate_gear(
            current_rpm, current_speed, current_load
        )
        data_store["Idle Indicator"] = idle_ready(current_rpm, current_speed)


def _build_csv_row(all_data, data_store):
    row = {
        "Time": datetime.now().astimezone().strftime("%H:%M:%S"),
        "OBD Connected": obd_state.is_connected,
    }
    for data in all_data:
        row[f"{data.name} ({data.unit})"] = data_store.get(data.name, 0)
    return row


def obd_worker(all_data, data_store, data_lock, csv_queue):
    """Background worker that polls sensors (OBD and Pi) based on
    priority and pushes rows to the CSV logger. Runs the same whether or
    not an OBD connection is present -- OBD sensors just contribute
    nothing (leaving prior/default values in data_store) until they're
    reachable.

    Args:
        all_data: List of ObdData/AddedData objects to query
        data_store: Shared dictionary of current sensor values
        data_lock: Lock guarding data_store
        csv_queue: Queue to send finished rows to the CSV logger
    """
    last_update_times = {data.name: 0 for data in all_data}
    last_csv_write = 0

    while True:
        try:
            current_time = time.time()
            local_updates = _poll_due_sensors(all_data, last_update_times, current_time)

            with data_lock:
                if local_updates:
                    data_store.update(local_updates)
                if obd_state.is_connected:
                    _update_calculated_fields(local_updates, data_store)
                else:
                    _reset_obd_fields(all_data, data_store)

                if current_time - last_csv_write >= CSV_WRITE_INTERVAL:
                    csv_queue.put(_build_csv_row(all_data, data_store))
                    last_csv_write = current_time

            time.sleep(LOOP_SLEEP)

        except (AttributeError, TypeError, KeyError) as e:
            # Expected data/formatting hiccups -- keep the thread alive
            logger.warning(f"OBD Thread Data Error: {e}")
            time.sleep(ERROR_BACKOFF)
        except Exception as e:  # noqa: BLE001
            # Unknown failure: log and keep going rather than killing the
            # thread, since that would also stop Pi data and CSV logging.
            logger.error(f"OBD Thread Unexpected Error: {e}")
            time.sleep(ERROR_BACKOFF)
