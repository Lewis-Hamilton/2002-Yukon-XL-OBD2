import obd
# import fake_obd as obd
import sys
import time
import csv
from utils import check_connection, celsius_to_fahrenheit, convert_to_number
from my_data import all_data
from datetime import datetime

print("Starting up...")


try:
    print("Connecting...")
    connection = obd.OBD(portstr="/dev/ttyUSB0")
    # connection = obd.FakeOBD()

    check_connection(connection)

    now = datetime.now()

    csv_name = now.date()
    column_names = [data.name for data in all_data]
    column_names.insert(0, "Time")
    with open (f"{csv_name}.csv", "w", newline="") as csvfile:
        thewriter = csv.DictWriter(csvfile, fieldnames=column_names)
        thewriter.writeheader()
        print(f"Logging data to '{csv_name}.csv'...")

        while True:
            try:
                then = datetime.now()
                data_row = {"Time": then.time()}

                for data in all_data:
                    data_row[data.name] = data.response
                thewriter.writerow(data_row)
                time.sleep(1)

            except KeyboardInterrupt:
                print("\nStopping")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(5)

finally:
    connection.close()
    print("Connection closed. Script finished.")