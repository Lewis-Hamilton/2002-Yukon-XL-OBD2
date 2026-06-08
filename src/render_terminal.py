import os

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

    throttle = data_store.get('Throttle Position', 0)
    load     = data_store.get('Engine Load', 0)
    gear     = data_store.get('Estimated Gear', '---')
    pi_cpu_temp = data_store.get('PI CPU Temperature')
    pi_cpu_usage = data_store.get('PI CPU Usage')
    pi_ram_usage = data_store.get('PI RAM Usage')
    gear_header, gear_fill = gear_indicator(gear, bar_width)

    # Engine load bar
    load_bar_fill = int((min(load, 100) / 100) * bar_width)
    load_bar      = '\u2588' * load_bar_fill + '\u2591' * (bar_width - load_bar_fill)

    # Throttle bar
    throttle_bar_fill = int((min(throttle, 100) / 100) * bar_width)
    throttle_bar      = '\u2588' * throttle_bar_fill + '\u2591' * (bar_width - throttle_bar_fill)

    # CPU bar
    cpu_bar_fill = int((min(pi_cpu_usage, 100) / 100) * bar_width)
    cpu_bar      = '\u2588' * cpu_bar_fill + '\u2591' * (bar_width - cpu_bar_fill)

    # RAM bar
    ram_bar_fill = int((min(pi_ram_usage, 100) / 100) * bar_width)
    ram_bar      = '\u2588' * ram_bar_fill + '\u2591' * (bar_width - ram_bar_fill)

    # Pi Temp bar
    pi_temp_bar_fill = int((min(pi_cpu_temp, 100) / 100) * bar_width)
    pi_temp_bar      = '\u2588' * pi_temp_bar_fill + '\u2591' * (bar_width - pi_temp_bar_fill)

    # Pi temp status
    if pi_cpu_temp is None:
        pi_str = '--C'
    else:
        pi_str = f'{pi_cpu_temp}C'

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
    lines.append(row(f'  PI Temperature: {pi_str}'))
    lines.append(row(f'  {pi_temp_bar}'))
    lines.append(row(f'  CPU: {pi_cpu_usage}%'))
    lines.append(row(f'  {cpu_bar}'))
    lines.append(row(f'  RAM: {pi_ram_usage}%'))
    lines.append(row(f'  {ram_bar}'))
    lines.append(divider)
    lines.append(row('  Ctrl+C to quit'))
    lines.append(divider)

    for line in lines:
        print(line)