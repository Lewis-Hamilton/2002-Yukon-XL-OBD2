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
    # column_names.append("Observed Ratio")
    column_names.append("Calculated Gear")

    speed = 0
    rpm = 0

    with open (csv_name, "w", newline="") as csvfile:
        thewriter = csv.DictWriter(csvfile, fieldnames=column_names)
        thewriter.writeheader()
        print(f"Logging data to '{csv_name}'...")

        while True:
            try:
                then = datetime.now()
                data_row = {"Time": then.time()}

                for data in all_data:
                    currentValue = data.response
                    data_row[f"{data.name} ({data.unit})"] = currentValue

                    # if data.name == "RPM":
                    #     rpm_num = currentValue
                    #     if rpm_num > 850:
                    #        print("Idle too high")
                    #     if rpm_num <= 850:
                    #        print("Idle dropped")
                    # if data.name == "Coolant Tempurature":
                    #     coolantF = currentValue
                    #     if coolantF < 195:
                    #         print("Coolant Cold")
                    #     if coolantF >= 195:
                    #         print("Coolant Warm")

                    # Constants based on 4L60E, 3.73 Axle, and 31.6" Tires
                    # CONST_FACTOR = 0.09395
                    # TOLERANCE = 0.45 # You may need to tune this value

                    if data.name == "RPM":
                        rpm = currentValue
                        print(f"{rpm} {data.unit}")
                    if data.name == "Speed":
                        speed = currentValue
                        print(f"{speed} {data.unit}")
                    if data.name == "Engine Load":
                        print(f"{currentValue} {data.unit}")

                    if speed == 0:
                        # Handle stationary or very low speed case (will be hard to tell 1st/Neutral/Park)
                        # The gear selector position is not readable via OBD-II
                        print("Vehicle is stopped or moving too slowly for gear calculation.")
                        # return
                        continue

                    AXLE_RATIO = 3.73 
                    TIRE_DIAMETER = 31.1
                    constant = 336.13

                    # OBSERVED_RATIO = (rpm / speed) * CONST_FACTOR

                    # if (11.41 - TOLERANCE) < OBSERVED_RATIO < (11.41 + TOLERANCE):
                    #     CURRENT_GEAR = "1st"
                    # elif (6.08 - TOLERANCE) < OBSERVED_RATIO < (6.08 + TOLERANCE):
                    #     CURRENT_GEAR = "2nd"
                    # elif (3.73 - TOLERANCE) < OBSERVED_RATIO < (3.73 + TOLERANCE):
                    #     CURRENT_GEAR = "3rd"
                    # elif (2.61 - TOLERANCE) < OBSERVED_RATIO < (2.61 + TOLERANCE):
                    #     CURRENT_GEAR = "4th (Overdrive)"
                    # else:
                    #     CURRENT_GEAR = "Unknown (Coast or Torque Converter Slip)"

                    RPM_PER_MPH_1ST = (AXLE_RATIO * 3.06 * constant) / TIRE_DIAMETER # ~123
                    RPM_PER_MPH_2ND = (AXLE_RATIO * 1.63 * constant) / TIRE_DIAMETER # ~65
                    RPM_PER_MPH_3RD = (AXLE_RATIO * 1.00 * constant) / TIRE_DIAMETER # ~40
                    RPM_PER_MPH_4TH = (AXLE_RATIO * 0.70 * constant) / TIRE_DIAMETER # ~28

                    if speed > 5:
                        current_ratio = rpm / speed
                        
                        # We use "midpoints" to decide the gear
                        if current_ratio > 90:
                            CURRENT_GEAR = "1st"
                        elif 52 < current_ratio <= 90:
                            CURRENT_GEAR = "2nd"
                        elif 34 < current_ratio <= 52:
                            CURRENT_GEAR = "3rd"
                        elif current_ratio <= 34:
                            CURRENT_GEAR = "4th (OD)"
                    else:
                        CURRENT_GEAR = "N/P"

                    data_row["Calculated Gear"] = CURRENT_GEAR
                    # print(f"Current RPM/MPH Observed Ratio: {OBSERVED_RATIO:.2f}")
                    print(f"Calculated Gear: {CURRENT_GEAR}")

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