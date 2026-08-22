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
STARTUP_SETTLE_TIME = 2  # Give OBD thread time to get first readings
CSV_SHUTDOWN_GRACE = 0.5  # Give CSV thread time to finish


def _start_worker_threads(connection, data_store, data_lock, args):
    """Starts the OBD-polling and CSV-logging threads and returns the
    csv_queue so the caller can signal shutdown later.
    """
    csv_queue = queue.Queue()

    obd_thread = threading.Thread(
        target=obd_worker,
        args=(connection, all_data, data_store, data_lock, csv_queue),
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
    """Runs the app once a live OBD connection is established: starts
    background threads, plays the intro animation, then loops rendering
    the terminal display until interrupted.

    `connector` is an OBDConnector that has already connected successfully.
    """
    data_lock = threading.Lock()
    data_store = {data.name: 0 for data in all_data}
    csv_queue = None

    try:
        _maybe_start_flask(args, data_store, data_lock)
        csv_queue = _start_worker_threads(
            connector.connection, data_store, data_lock, args
        )

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
        print("Connection closed. Script finished.")
