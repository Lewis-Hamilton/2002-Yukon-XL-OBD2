import sys
import os
import time
import queue
import threading
from args import parser
from utils import check_connection
from my_data import all_data
from obd_worker import obd_worker
from csv_logger import csv_logger
from render_terminal import render_terminal, data_animation
from stereo_screen import hide_cursor, show_cursor
from startup_screen import startup_screen

args = parser.parse_args()

if args.testing or args.manual_testing:
    import fake_obd as obd
else:
    import obd
    
os.system('clear')
hide_cursor()

# Set up connection variables
connection = None
connection_error = None

def connect_obd():
    global connection, connection_error
    try:
        if args.testing == True or args.manual_testing == True:
            connection = obd.FakeOBD()
        else:
            connection = obd.OBD()
        check_connection(connection)
    except Exception as e:
        connection_error = e

# Start connecting in background
connect_thread = threading.Thread(target=connect_obd, daemon=True)
connect_thread.start()

# Play animation while connection happens, passing thread and csv check
startup_screen(connect_thread)

# Handle connection result
if connection_error:
    raise connection_error

if connection is None:
    raise ConnectionError("OBD connection timed out")

try:
    data_lock = threading.Lock()
    data_store = {data.name: 0 for data in all_data}
    csv_queue = queue.Queue()

    if args.manual_testing:
        from flask_server import start_flask
        start_flask(data_store, data_lock)

    # Start OBD Thread
    obd_thread = threading.Thread(
        target=obd_worker,
        args=(connection, all_data, data_store, data_lock, csv_queue),
        daemon=True
    )
    obd_thread.start()

    # Start CSV Thread
    csv_thread = threading.Thread(
        target=csv_logger,
        args=(csv_queue, all_data, args),
        daemon=True
    )
    csv_thread.start()

    time.sleep(2)  # Give OBD thread time to get first readings
    data_animation()

    while True:
        with data_lock:
            current_snapshot = data_store.copy()
        render_terminal(current_snapshot)
        time.sleep(0.1)  # How fast to draw the output

except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Fatal error: {e}")
finally:
    show_cursor()
    csv_queue.put(None)  # Tell CSV thread to stop
    time.sleep(0.5)      # Give CSV thread time to finish
    if connection:
        try:
            connection.close()
        except Exception:
            pass
    print("Connection closed. Script finished.")