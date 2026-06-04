import os
import sys
import time
import queue
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

def get_pi_cpu_temp():
    """Read Raspberry Pi CPU temperature in Celsius"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_milli_c = int(f.read().strip())
            temp_c = temp_milli_c / 1000.0
            return round(temp_c, 1)
    except Exception:
        return None


def render_terminal(data_store):
    """
    Render all gauge data as large, readable terminal text.
    Clears the screen each time so it updates in place.
    """
    os.system('clear')

    rpm      = data_store.get('RPM', 0)
    speed    = data_store.get('Speed', 0)
    coolant  = data_store.get('Coolant Temperature', 0)
    throttle = data_store.get('Throttle Position', 0)
    voltage  = data_store.get('Voltage', 0)
    gear     = data_store.get('Estimated Gear', '---')
    pi_temp  = get_pi_cpu_temp()

    # Build shift bar (20 chars wide)
    bar_fill = int((min(rpm, 6000) / 6000) * 20)
    bar      = '\u2588' * bar_fill + '\u2591' * (20 - bar_fill)
    redline  = '  *** REDLINE ***' if rpm > 5000 else ''

    # Voltage status
    try:
        v = float(str(voltage).replace('V', '').strip())
        if v >= 13.0:
            voltage_status = '(OK)'
        elif v >= 12.0:
            voltage_status = '(LOW)'
        else:
            voltage_status = '(CRITICAL)'
    except (ValueError, TypeError):
        voltage_status = ''

    # Coolant status
    coolant_status = '(COLD)' if coolant < 195 else '(WARM)'

    # Pi temp status
    if pi_temp is None:
        pi_temp_str = '--'
        pi_status   = ''
    else:
        pi_temp_str = f'{pi_temp}C'
    if pi_temp < 65:
        pi_status = '(OK)'
    elif pi_temp < 75:
        pi_status = '(WARM)'
    else:
        pi_status = '(HOT!)'

    print()
    print('============================')
    print(f'  RPM:      {rpm}')
    print(f'  [{bar}]{redline}')
    print('============================')
    print(f'  SPEED:    {speed} MPH')
    print(f'  GEAR:     {gear}')
    print('============================')
    print(f'  COOLANT:  {coolant}F  {coolant_status}')
    print(f'  THROTTLE: {throttle}%')
    print(f'  VOLTAGE:  {voltage}V  {voltage_status}')
    print('============================')
    print(f'  PI TEMP:  {pi_temp_str}  {pi_status}')
    print('============================')
    print()
    print('  Press Ctrl+C to quit')


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
        time.sleep(0.5)  # Refresh twice per second

except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(f"Fatal error: {e}")
finally:
    csv_queue.put(None)  # Tell CSV thread to stop
    time.sleep(0.5)      # Give CSV thread time to finish
    connection.close()
    print("Connection closed. Script finished.")