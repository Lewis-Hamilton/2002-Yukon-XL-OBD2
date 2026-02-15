import sys
import time
import csv
import os
import queue
from args import parser
from utils import check_connection, celsius_to_fahrenheit, convert_to_number, get_filename, create_logging_dir
from my_data import all_data
from datetime import datetime
import pygame
import threading

# Import obd based on testing vs real world
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

    def csv_logger():
        """Separate thread that writes data to CSV"""
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
        
        with open(csv_name, "w", newline="") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames=column_names)
            thewriter.writeheader()
            print(f"Logging data to '{csv_name}'...")
            
            while True:
                try:
                    # Wait for data from the queue (blocks until data available)
                    data_row = csv_queue.get(timeout=1)
                    
                    if data_row is None:  # Poison pill to stop the thread
                        print("CSV logger stopping...")
                        break
                    
                    thewriter.writerow(data_row)
                    csvfile.flush()  # Make sure it's written to disk immediately
                    
                except queue.Empty:
                    # No data in queue, just continue
                    continue
                except Exception as e:
                    print(f"CSV Thread Error: {e}")
                    time.sleep(1)

    def obd_worker():
        """OBD worker thread that queries sensors based on priority"""
        # Track when each sensor was last updated
        last_update_times = {data.name: 0 for data in all_data}
        last_csv_write = 0
        
        # Define update intervals for each priority (in seconds)
        priority_intervals = {
            "fast": 0.5,    # Update twice per second, increase time if errors
            "medium": 2.0,  # Update every 2 seconds
            "slow": 10.0    # Update every 10 seconds
        }
        
        while True:
            try:
                current_time = time.time()
                
                # Update sensors based on their priority
                for data in all_data:
                    time_since_update = current_time - last_update_times[data.name]
                    interval = priority_intervals.get(data.priority, 5.0)
                    
                    # Should we update this sensor now?
                    if time_since_update >= interval:
                        val = data.response  # Query the car
                        data_store[data.name] = val
                        last_update_times[data.name] = current_time
                
                # Write to CSV every 1 second
                if current_time - last_csv_write >= 1.0:
                    data_row = {"Time": datetime.now().time()}
                    
                    for data in all_data:
                        data_row[f"{data.name} ({data.unit})"] = data_store.get(data.name, 0)
                    
                    csv_queue.put(data_row)  # Send to CSV thread
                    last_csv_write = current_time
                
                time.sleep(0.05)  # Small sleep to prevent CPU hammering
                
            except Exception as e:
                print(f"OBD Thread Error: {e}")
                time.sleep(1)

    # Start OBD Thread
    obd_thread = threading.Thread(target=obd_worker, daemon=True)
    obd_thread.start()
    
    # Start CSV Thread
    csv_thread = threading.Thread(target=csv_logger, daemon=True)
    csv_thread.start()

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((480, 320))  # Typical 3.5" display size
    font_large = pygame.font.SysFont("Arial", 60)
    font_small = pygame.font.SysFont("Arial", 30)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Black background

        # Draw RPM (Digital)
        rpm_value = data_store.get('RPM', 0)
        rpm_text = font_large.render(f"RPM: {rpm_value}", True, (0, 255, 0))
        screen.blit(rpm_text, (20, 20))
        
        # Draw RPM shift bar
        bar_width = min((rpm_value / 6000) * 400, 400)  # Cap at 400px
        bar_color = (255, 0, 0) if rpm_value > 5000 else (0, 255, 0)
        pygame.draw.rect(screen, bar_color, (40, 100, bar_width, 40))
        
        # Draw Speed
        speed_value = data_store.get('Speed', 0)
        speed_text = font_small.render(f"Speed: {speed_value} MPH", True, (255, 255, 0))
        screen.blit(speed_text, (20, 160))
        
        # Draw Coolant Temperature
        coolant_value = data_store.get('Coolant Temperature', 0)
        coolant_color = (0, 255, 255) if coolant_value < 195 else (255, 100, 0)
        coolant_text = font_small.render(f"Coolant: {coolant_value}°F", True, coolant_color)
        screen.blit(coolant_text, (20, 200))
        
        # Draw Throttle Position
        throttle_value = data_store.get('Throttle Position', 0)
        throttle_text = font_small.render(f"Throttle: {throttle_value}%", True, (255, 255, 255))
        screen.blit(throttle_text, (20, 240))

        pygame.display.flip()
        clock.tick(30)  # Limit to 30 FPS

except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(f"Fatal error: {e}")
finally:
    csv_queue.put(None)  # Tell CSV thread to stop
    time.sleep(0.5)  # Give CSV thread time to finish
    connection.close()
    print("Connection closed. Script finished.")