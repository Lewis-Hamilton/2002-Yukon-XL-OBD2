import os
import sys
import time
import queue
import subprocess
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

def get_pi_stats():
    """Get Raspberry Pi CPU and RAM usage"""
    import psutil
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    ram_used = round(ram.used / 1024 / 1024)   # Convert to MB
    ram_total = round(ram.total / 1024 / 1024)  # Convert to MB
    ram_percent = ram.percent
    return cpu, ram_used, ram_total, ram_percent

def get_pi_cpu_temp():
    """Read Raspberry Pi CPU temperature in Celsius"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_milli_c = int(f.read().strip())
            temp_c = temp_milli_c / 1000.0
            return round(temp_c, 1)
    except Exception:
        return None


def figlet(text):
    """Render text using figlet for large terminal display"""
    try:
        result = subprocess.run(['figlet', str(text)], capture_output=True, text=True)
        return result.stdout
    except Exception:
        return f"  {text}\n"  # Fallback if figlet fails


def render_terminal(data_store):
    """
    Render gauge data as readable terminal text.
    """
    os.system('clear')

    speed    = data_store.get('Speed', 0)
    coolant  = data_store.get('Coolant Temperature', 0)
    throttle = data_store.get('Throttle Position', 0)
    voltage  = data_store.get('Voltage', 0)
    load     = data_store.get('Engine Load', 0)
    gear     = data_store.get('Estimated Gear', '---')
    pi_temp  = get_pi_cpu_temp()
    cpu, ram_used, ram_total, ram_percent = get_pi_stats()

    # Engine load bar (90 chars wide)
    bar_fill = int((min(load, 100) / 100) * 54)
    bar      = '\u2588' * bar_fill + '\u2591' * (54 - bar_fill)

    # Voltage status
    try:
        v = float(str(voltage).replace('V', '').strip())
        if v >= 13.0:
            voltage_status = '(OK)'
        elif v >= 12.0:
            voltage_status = '(LOW)'
        else:
            voltage_status = '(CRIT)'
    except (ValueError, TypeError):
        voltage_status = ''

    # Coolant status
    coolant_status = '(COLD)' if coolant < 195 else '(WARM)'

    # Pi temp status
    if pi_temp is None:
        pi_str = '--C'
        pi_status = ''
    else:
        pi_str = f'{pi_temp}C'
        if pi_temp < 65:
            pi_status = '(OK)'
        elif pi_temp < 75:
            pi_status = '(WARM)'
        else:
            pi_status = '(HOT!)'

    # Build lines - each must fit inside 58 chars (60 minus 2 border chars)
    WIDTH = 58
    divider = '+' + '-' * WIDTH + '+'

    def row(text=''):
        # Pad or truncate to exactly WIDTH chars
        return '|' + text.ljust(WIDTH)[:WIDTH] + '|'

    # Get figlet output and split into lines
    gear_figlet = figlet(gear).rstrip('\n').split('\n')

    lines = []
    lines.append(divider)
    lines.append(row(f'  LOAD: {load}%'))
    lines.append(row(f'  {bar}'))
    lines.append(divider)
    for gear_line in gear_figlet:
        lines.append(row(gear_line))
    lines.append(divider)
    lines.append(row(f'  Coolant: {coolant}F {coolant_status}   Throttle: {throttle}%'))
    lines.append(row(f'  Voltage: {voltage}V {voltage_status}   Pi: {pi_str} {pi_status}'))
    lines.append(row(f'  CPU: {cpu}%   RAM: {ram_used}MB/{ram_total}MB ({ram_percent}%)'))
    lines.append(divider)
    lines.append(row('  Ctrl+C to quit'))
    lines.append(divider)

    for line in lines:
        print(line)

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