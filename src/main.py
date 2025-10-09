import sys
import time
import csv
import os
from args import parser
from utils import check_connection, celsius_to_fahrenheit, convert_to_number, get_filename
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

# move this to util function
    if os.path.exists("./logged_data"):
        print("Logging directory exists")
    else:
        print("Logging directory does not exist, creating now")   
        os.mkdir("./logged_data") 

    now = datetime.now()

    current_date = now.date()
    initial_csv_name = f"./logged_data/{current_date}.csv"
    csv_name = get_filename(initial_csv_name)
    column_names = [data.name for data in all_data]
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
                    data_row[data.name] = data.response
                    if data.name == "RPM":
                        rpm_response = str(data.response)
                        new_rpm = rpm_response.replace(" revolutions_per_minute", "")
                        rpm_num = float(new_rpm)
                        if rpm_num > 850:
                           print("Engine Speed: Not Ready")
                        if rpm_num <= 850:
                           print("Engine Speed: Ready")
                    # This doesn't work yet
                    # if data.name == "COOLANT_TEMP":
                    #     coolant_response = str(data.response)
                    #     new_coolant = coolant_response.replace(" degree_Celsius", "")
                    #     coolant_num = int(new_coolant)
                    #     if coolant_num < 88:
                    #         print("Coolant Temp: Not Ready")
                    #     if coolant_num >= 88:
                    #         print("Coolant Temp: Ready")

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