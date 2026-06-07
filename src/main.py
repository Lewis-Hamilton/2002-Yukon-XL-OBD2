import time
import os
import queue
import threading
from args import parser
from utils import check_connection
from my_data import all_data
from obd_worker import obd_worker
from csv_logger import csv_logger

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

    data_store = {data.name: 0 for data in all_data}
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

    while True:
        try:
            rpm = data_store.get('RPM', 0)
            if rpm > 850:
                print("Idle too high")
            else:
                print("Idle dropped")

            coolant = data_store.get('Coolant Temperature', 0)
            if coolant < 195:
                print("Coolant Cold")
            else:
                print("Coolant Warm")

            time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping")
            break

except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(f"Fatal error: {e}")
finally:
    csv_queue.put(None)
    time.sleep(0.5)
    connection.close()
    print("Connection closed. Script finished.")