import time
from stereo_screen import print_screen
from idle_calc import idle_ready
from gear_calc import estimate_gear

BAR_WIDTH = 54

def loading_bar():
    BLOCK_WIDTH = 20
    BAR_SPEED = 30
    travel = BAR_WIDTH - BLOCK_WIDTH
    period = travel * 2
    position = int(time.time() * BAR_SPEED) % period
    if position >= travel:
        position = period - position
    return '\u2591' * position + '\u2588' * BLOCK_WIDTH + '\u2591' * (BAR_WIDTH - BLOCK_WIDTH - position)

def idle_indicator(idle_status):
    if idle_status:
        return '\u2588' * BAR_WIDTH
    else:
        return loading_bar()

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

    active = gear_map.get(gear, 0)

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

    header = '┃'
    fill   = '┃'

    for i, (g, w) in enumerate(zip(gears, widths)):
        dashes = w - len(g)
        left   = dashes // 2
        right  = dashes // 2
        header += '━' * left + g + '━' * right

        if i == active:
            fill += '\u2588' * w
        else:
            fill += ' ' * w

        header += '┃'
        fill   += '┃'

    return header, fill

_gear_stats = {
    "current_gear": None,
    "min_ratio": None,
    "max_ratio": None,
}

def gear_ratio_stats(gear, rpm, speed):
    if speed == 0 or rpm == 0:
        return _gear_stats["min_ratio"], _gear_stats["max_ratio"]

    ratio = rpm / speed

    if gear != _gear_stats["current_gear"]:
        _gear_stats["current_gear"] = gear
        _gear_stats["min_ratio"] = ratio
        _gear_stats["max_ratio"] = ratio
    else:
        if ratio < _gear_stats["min_ratio"]:
            _gear_stats["min_ratio"] = ratio
        if ratio > _gear_stats["max_ratio"]:
            _gear_stats["max_ratio"] = ratio

    return round(_gear_stats["min_ratio"], 2), round(_gear_stats["max_ratio"], 2)

def progress_bar(bar_data):
    bar_fill = int((min(bar_data, 100) / 100) * BAR_WIDTH)
    bar      = '\u2588' * bar_fill + '\u2591' * (BAR_WIDTH - bar_fill)
    return bar

def render_terminal(data_store):
    """
    Render gauge data as readable terminal text.
    """

    throttle = data_store.get('Throttle Position', 0)
    load     = data_store.get('Engine Load', 0)
    gear     = data_store.get('Estimated Gear', '---')
    test_rpm = data_store.get('RPM', 0)
    test_speed = data_store.get('Speed', 0)
    idle_status = data_store.get('Idle Indicator')
    pi_cpu_temp = data_store.get('PI CPU Temperature')
    pi_cpu_usage = data_store.get('PI CPU Usage')
    pi_ram_usage = data_store.get('PI RAM Usage')
    gear_header, gear_fill = gear_indicator(gear, BAR_WIDTH)
    idle_bar = idle_indicator(idle_status)

    if test_rpm != 0 or test_speed != 0:
        current_ratio = test_rpm / test_speed
    else:
        current_ratio = 0
    test_gear = estimate_gear(test_rpm, test_speed)
    gear_header2, gear_fill2 = gear_indicator(test_gear, BAR_WIDTH)
    min_ratio, max_ratio = gear_ratio_stats(test_gear, test_rpm, test_speed)

    # Pi temp status
    if pi_cpu_temp is None:
        pi_str = '--C'
    else:
        pi_str = f'{pi_cpu_temp}C'

    divider = '━' * BAR_WIDTH

    lines = []
    lines.append("Idle Status")
    lines.append(idle_bar)
    lines.append(divider)
    lines.append(gear_header)
    lines.append(gear_fill)
    lines.append(gear_header2)
    lines.append(gear_fill2)
    lines.append(divider)
    lines.append(f'LOAD: {load}%')
    lines.append(progress_bar(load))
    lines.append(f'THROTTLE: {throttle}%')
    lines.append(progress_bar(throttle))
    lines.append(divider)
    lines.append(f'PI Temperature: {pi_str}')
    lines.append(progress_bar(pi_cpu_temp))
    # lines.append(f'CPU: {pi_cpu_usage}%')
    # lines.append(progress_bar(pi_cpu_usage))
    lines.append(f'Current Ratio: {current_ratio}')
    lines.append(f'Min Ratio: {min_ratio}')
    lines.append(f'Max Ratio: {max_ratio}')
    # lines.append(f'RAM: {pi_ram_usage}%')
    # lines.append(progress_bar(pi_ram_usage))

    print_screen(lines)

def data_animation():
    """Sweep all bars from 0 to 100 and back, cycle through gears"""
    gears = ['N/P', '1st', '2nd', '3rd', '4th (OD)', '3rd', '2nd', '1st', 'N/P']
    steps = list(range(0, 101, 5)) + list(range(100, -1, -5))
    
    for i, value in enumerate(steps):
        fake_store = {
            'Engine Load': 0,
            'Throttle Position': 0,
            'PI CPU Temperature': 0,
            'PI CPU Usage': 0,
            'PI RAM Usage': 0,
            'Estimated Gear': 'N/P',
        }
        fake_store['Engine Load'] = value
        fake_store['Throttle Position'] = value
        fake_store['PI CPU Temperature'] = value
        fake_store['PI CPU Usage'] = value
        fake_store['PI RAM Usage'] = value
        
        # Cycle through gears based on progress
        gear_index = int((i / len(steps)) * len(gears))
        fake_store['Estimated Gear'] = gears[min(gear_index, len(gears) - 1)]
        
        render_terminal(fake_store)
        time.sleep(0.07)