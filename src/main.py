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
import random


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
    ram_percent = ram.percent
    return cpu, ram_percent

def get_pi_cpu_temp():
    """Read Raspberry Pi CPU temperature in Celsius"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_milli_c = int(f.read().strip())
            temp_c = temp_milli_c / 1000.0
            return round(temp_c, 1)
    except Exception:
        return None

bar_width = 54

def gear_indicator(gear, bar_width):
    gears = ['NONE', '1st', '2nd', '3rd', '4th']
    gear_map = {
        '1st':      1,
        '2nd':      2,
        '3rd':      3,
        '4th (OD)': 4,
        'N/P':      0,
        '---':      0,
    }

    active = gear_map.get(gear, 4)

    # Account for opening |, 4 inner dividers, closing |
    total = bar_width - 6
    base  = total // 4

    # Make sure base - len(gear_label) is always even
    # '1st', '2nd', '3rd', '4th' are all 3 chars
    # so base - 3 must be even, meaning base must be odd
    if (base - 3) % 2 != 0:
        base -= 1

    na_width = total - (base * 4)  # N/A gets whatever is left

    widths = [na_width, base, base, base, base]

    header = '|'
    fill   = '|'

    for i, (g, w) in enumerate(zip(gears, widths)):
        dashes = w - len(g)
        left   = dashes // 2
        right  = dashes // 2
        header += '-' * left + g + '-' * right

        if i == active:
            fill += '\u2588' * w
        else:
            fill += ' ' * w

        header += '|'
        fill   += '|'

    return header, fill

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
    gear_header, gear_fill = gear_indicator(gear, bar_width)

    cpu, ram_percent = get_pi_stats()

    # Engine load bar
    load_bar_fill = int((min(load, 100) / 100) * bar_width)
    load_bar      = '\u2588' * load_bar_fill + '\u2591' * (bar_width - load_bar_fill)

    # Throttle bar
    throttle_bar_fill = int((min(throttle, 100) / 100) * bar_width)
    throttle_bar      = '\u2588' * throttle_bar_fill + '\u2591' * (bar_width - throttle_bar_fill)

    # CPU bar
    cpu_bar_fill = int((min(cpu, 100) / 100) * bar_width)
    cpu_bar      = '\u2588' * cpu_bar_fill + '\u2591' * (bar_width - cpu_bar_fill)

    # RAM bar
    ram_bar_fill = int((min(ram_percent, 100) / 100) * bar_width)
    ram_bar      = '\u2588' * ram_bar_fill + '\u2591' * (bar_width - ram_bar_fill)

    # Pi Temp bar
    pi_temp_bar_fill = int((min(pi_temp, 100) / 100) * bar_width)
    pi_temp_bar      = '\u2588' * pi_temp_bar_fill + '\u2591' * (bar_width - pi_temp_bar_fill)

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
    else:
        pi_str = f'{pi_temp}C'

    # Build lines - each must fit inside 58 chars (60 minus 2 border chars)
    WIDTH = 58
    divider = '+' + '-' * WIDTH + '+'

    def row(text=''):
        # Pad or truncate to exactly WIDTH chars
        return '|' + text.ljust(WIDTH)[:WIDTH] + '|'

    lines = []
    lines.append(divider)
    lines.append(row(f'  {gear_header}'))
    lines.append(row(f'  {gear_fill}'))
    lines.append(divider)
    lines.append(row(f'  LOAD: {load}%'))
    lines.append(row(f'  {load_bar}'))
    lines.append(row(f'  THROTTLE: {throttle}%'))
    lines.append(row(f'  {throttle_bar}'))
    lines.append(divider)
    lines.append(row(f'  Coolant: {coolant}F {coolant_status}'))
    lines.append(row(f'  Voltage: {voltage}V {voltage_status}'))
    lines.append(row(f'  PI Temperature: {pi_str}'))
    lines.append(row(f'  {pi_temp_bar}'))
    lines.append(row(f'  CPU: {cpu}%'))
    lines.append(row(f'  {cpu_bar}'))
    lines.append(row(f'  RAM: {ram_percent}%'))
    lines.append(row(f'  {ram_bar}'))
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