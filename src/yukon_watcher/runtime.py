import queue
import threading
import time

from yukon_watcher.data_outputs.csv_logger import csv_logger
from yukon_watcher.display_outputs.render_terminal import (
    data_animation,
    render_terminal,
)
from yukon_watcher.display_outputs.stereo_screen import show_cursor
from yukon_watcher.obd_utils.my_data import all_data
from yukon_watcher.obd_utils.obd_worker import obd_worker

RENDER_INTERVAL = 0.1  # How fast to draw the output
STARTUP_SETTLE_TIME = 2  # Give worker thread time to get first readings
CSV_SHUTDOWN_GRACE = 0.5  # Give CSV thread time to finish


def _start_worker_threads(data_store, data_lock, args):
    """Starts the sensor-polling and CSV-logging threads and returns the
    csv_queue so the caller can signal shutdown later. Runs the same
    whether or not OBD is connected -- see obd_worker/my_data.
    """
    csv_queue = queue.Queue()

    obd_thread = threading.Thread(
        target=obd_worker,
        args=(all_data, data_store, data_lock, csv_queue),
        daemon=True,
    )
    obd_thread.start()

    csv_thread = threading.Thread(
        target=csv_logger, args=(csv_queue, all_data, args), daemon=True
    )
    csv_thread.start()

    return csv_queue


def _maybe_start_flask(args, data_store, data_lock):
    if not args.manual_testing:
        return
    from flask_server import start_flask

    start_flask(data_store, data_lock)


def _render_loop(data_store, data_lock):
    while True:
        with data_lock:
            current_snapshot = data_store.copy()
        render_terminal(current_snapshot)
        time.sleep(RENDER_INTERVAL)


def run(connector, args):
    """Runs the app: starts background threads, plays the intro
    animation, then loops rendering the terminal display until
    interrupted.

    Works whether or not `connector` ended up with a live OBD
    connection -- OBD gauges just hold their default values (see
    my_data.ObdData.response) until/unless one is available. Pi data
    and CSV logging run unconditionally.
    """
    data_lock = threading.Lock()
    data_store = {data.name: 0 for data in all_data}
    csv_queue = None

    try:
        _maybe_start_flask(args, data_store, data_lock)
        csv_queue = _start_worker_threads(data_store, data_lock, args)

        time.sleep(STARTUP_SETTLE_TIME)
        data_animation()

        _render_loop(data_store, data_lock)

    except KeyboardInterrupt:
        print("\nStopping...")

    except (OSError, RuntimeError) as e:
        import traceback

        traceback.print_exc()
        print(f"Fatal error: {e}")

    finally:
        show_cursor()
        if csv_queue is not None:
            csv_queue.put(None)  # Tell CSV thread to stop
            time.sleep(CSV_SHUTDOWN_GRACE)

        connector.close()
        print("Script finished.")
