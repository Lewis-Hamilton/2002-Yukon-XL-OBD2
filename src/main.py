import sys
import time
import csv
import os
from args import parser
from utils import check_connection, celsius_to_fahrenheit, convert_to_number, get_filename, create_logging_dir
from my_data import all_data
from datetime import datetime
import pygame
import threading

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

    def obd_worker():
        tick = 0
        while True:
            try:

                for data in all_data:
                    # Use your existing logic that returns the "usable number"
                    val = data.response
                    data_store[data.name] = val
                    time.sleep(0.2)
                rpm = data_store.get("RPM", 0)
                speed = data_store.get("Speed", 0)
                
                
            except Exception as e:
                print(f"OBD Thread Error: {e}")
                time.sleep(1)
            print(f"{data_store.get('RPM')}")
            time.sleep(0.1) # Don't choke the CPU

    # Start OBD Thread
    t = threading.Thread(target=obd_worker, daemon=True)
    t.start()

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((480, 320)) # Typical 3.5" display size
    font = pygame.font.SysFont("Arial", 80)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0)) # Black background

        # Draw RPM (Digital)
        rpm_text = font.render(f"RPM: {data_store['RPM']}", True, (0, 255, 0))
        screen.blit(rpm_text, (50, 50))
        
        # Draw a simple "Shift Bar"
        bar_width = (data_store['RPM'] / 6000) * 400
        pygame.draw.rect(screen, (255, 0, 0), (40, 150, bar_width, 50))

        pygame.display.flip()


    # create_logging_dir()

    # now = datetime.now()

    # current_date = now.date()
    # if args.testing == True:
    #     initial_csv_name = f"./logged_data/test-data-{current_date}.csv"
    # else:
    #     initial_csv_name = f"./logged_data/{current_date}.csv"
    # csv_name = get_filename(initial_csv_name)
    # column_names = [f"{data.name} ({data.unit})" for data in all_data]
    # column_names.insert(0, "Time")

    # with open (csv_name, "w", newline="") as csvfile:
    #     thewriter = csv.DictWriter(csvfile, fieldnames=column_names)
    #     thewriter.writeheader()
    #     print(f"Logging data to '{csv_name}'...")

    #     while True:
    #         try:
    #             then = datetime.now()
    #             data_row = {"Time": then.time()}

    #             for data in all_data:
    #                 currentValue = data.response
    #                 data_row[f"{data.name} ({data.unit})"] = currentValue

    #                 if data.name == "RPM":
    #                     rpm_num = currentValue
    #                     if rpm_num > 850:
    #                        print("Idle too high")
    #                     if rpm_num <= 850:
    #                        print("Idle dropped")
    #                 if data.name == "Coolant Tempurature":
    #                     coolantF = currentValue
    #                     if coolantF < 195:
    #                         print("Coolant Cold")
    #                     if coolantF >= 195:
    #                         print("Coolant Warm")

    #             thewriter.writerow(data_row)
    #             csvfile.flush()
    #             time.sleep(1)

    #         except KeyboardInterrupt:
    #             print("\nStopping")
    #             break
    #         except Exception as e:
    #             print(f"An error occurred: {e}")
    #             time.sleep(5)

finally:
    connection.close()
    print("Connection closed. Script finished.")