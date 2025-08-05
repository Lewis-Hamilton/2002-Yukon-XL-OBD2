import obd
import sys
import time
from utils import check_connection, celsius_to_fahrenheit, convert_to_number
from my_data import all_data, engine_load

connection = obd.OBD(portstr="/dev/ttyUSB0")

check_connection(connection)

while True:
    try:
        print(f"{engine_load.name}: {engine_load.response}", end="\r")
        sys.stdout.flush()
        time.sleep(3)

    except KeyboardInterrupt:
        print("\nStopping")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)