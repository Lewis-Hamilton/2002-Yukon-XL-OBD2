import sys
import time
import csv
import os
from args import parser
from utils import check_connection, celsius_to_fahrenheit, convert_to_number, get_filename, create_logging_dir
from my_data import all_data
from datetime import datetime

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

    create_logging_dir()

    now = datetime.now()

    current_date = now.date()
    if args.testing == True:
        initial_csv_name = f"./logged_data/test-data-{current_date}.csv"
    else:
        initial_csv_name = f"./logged_data/{current_date}.csv"
    csv_name = get_filename(initial_csv_name)
    column_names = [f"{data.name} ({data.unit})" for data in all_data]
    column_names.insert(0, "Time")

    with open (csv_name, "w", newline="") as csvfile:
        thewriter = csv.DictWriter(csvfile, fieldnames=column_names)
        thewriter.writeheader()
        print(f"Logging data to '{csv_name}'...")

        while True:
            try:
                then = datetime.now()
                data_row = {"Time": then.time()}

                for data in all_data:
                    response = data.response(connection)
                    data_row[f"{data.name} ({data.unit})"] = response
                thewriter.writerow(data_row)
                csvfile.flush()
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