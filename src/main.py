import sys
import time
import queue
import threading
from args import parser
from utils import check_connection
from my_data import all_data
from obd_worker import obd_worker
from csv_logger import csv_logger
from render_terminal import render_terminal

args = parser.parse_args()

if args.testing == True:
    import fake_obd as obd
else:
    import obd

print("Starting up...")

try:
    print("Connecting...")

    if args.testing == True:
        print("Running in test mode with fake obd data")
        connection = obd.FakeOBD()
    else:
        connection = obd.OBD(portstr="/dev/ttyUSB0")

    check_connection(connection)

    # Data store shared between threads
    data_store = {data.name: 0 for data in all_data}

    # Queue for passing data from OBD thread to CSV thread
    csv_queue = queue.Queue()

    # Start OBD Thread
    obd_thread = threading.Thread(
        target=obd_worker,
        args=(connection, all_data, data_store, csv_queue),
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

    print("Running! Data will appear shortly...")
    time.sleep(2)  # Give OBD thread time to get first readings

    while True:
        render_terminal(data_store)
        time.sleep(0.75)  # Need to update in obd_worker as well

except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(f"Fatal error: {e}")
finally:
    csv_queue.put(None)  # Tell CSV thread to stop
    time.sleep(0.5)      # Give CSV thread time to finish
    connection.close()
    print("Connection closed. Script finished.")