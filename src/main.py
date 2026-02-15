import sys
import time
import queue
import pygame
import threading
from args import parser
from utils import check_connection
from my_data import all_data
from obd_worker import obd_worker
from csv_logger import csv_logger

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

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((480, 320))  # Typical 3.5" display size
    font_large = pygame.font.SysFont("Arial", 60)
    font_small = pygame.font.SysFont("Arial", 30)
    clock = pygame.time.Clock()

    print("Display started - press X to quit")

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