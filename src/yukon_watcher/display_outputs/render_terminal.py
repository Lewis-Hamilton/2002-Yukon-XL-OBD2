import time

from yukon_watcher.display_outputs.stereo_screen import print_screen
from yukon_watcher.obd_utils import obd_state

BAR_WIDTH = 54
CONNECTION_BAR_WIDTH = len("OBD CONNECTION")
SPACING = 2
IDLE_BAR_WIDTH = BAR_WIDTH - CONNECTION_BAR_WIDTH - SPACING  # 38


def loading_bar(width):
    BLOCK_WIDTH = min(15, width)
    BAR_SPEED = 30
    travel = width - BLOCK_WIDTH
    period = travel * 2
    position = int(time.time() * BAR_SPEED) % period
    if position >= travel:
        position = period - position
    return (
        "\u2591" * position
        + "\u2588" * BLOCK_WIDTH
        + "\u2591" * (width - BLOCK_WIDTH - position)
    )


def idle_indicator(idle_status, width):
    if idle_status is None:
        return "\u2591" * width
    if idle_status:
        return "\u2588" * width
    return loading_bar(width)


def connection_indicator(is_connected, width):
    if is_connected:
        return "\u2588" * width
    return "\u2591" * width


def progress_bar(val, min_val=0, max_val=100):
    """
    Renders a gauge bar scaled to any custom [min_val, max_val] range.
    """
    if val is None:
        return "\u2591" * BAR_WIDTH

    # Clamp value within [min_val, max_val] bounds
    clamped_val = max(min_val, min(val, max_val))

    # Calculate zero-to-one ratio across the custom scale
    pct = (clamped_val - min_val) / (max_val - min_val)

    bar_fill = int(pct * BAR_WIDTH)
    bar = "\u2588" * bar_fill + "\u2591" * (BAR_WIDTH - bar_fill)
    return bar


def render_terminal(data_store):
    """
    Render gauge data as readable terminal text.
    """

    throttle = data_store.get("Throttle Position", 0)
    load = data_store.get("Engine Load", 0)
    idle_status = data_store.get("Idle Indicator")
    pi_cpu_temp = data_store.get("PI CPU Temperature")
    pi_cpu_usage = data_store.get("PI CPU Usage")
    pi_ram_usage = data_store.get("PI RAM Usage")
    driver_side_engine_bay_temperature = data_store.get(
        "Driver Side Engine Bay Temperature"
    )

    idle_bar = idle_indicator(idle_status, IDLE_BAR_WIDTH)
    conn_bar = connection_indicator(obd_state.is_connected, CONNECTION_BAR_WIDTH)

    # Pi temp status
    if pi_cpu_temp is None:
        pi_str = "--C"
    else:
        pi_str = f"{pi_cpu_temp}C"

    # DS18B20 Temp string formatting
    if driver_side_engine_bay_temperature is None:
        ds18_str = "--F"
    else:
        ds18_str = f"{driver_side_engine_bay_temperature:.1f}F"

    divider = "━" * BAR_WIDTH

    lines = []
    # Combined line for headers and status bars
    lines.append(
        f"{'OBD CONNECTION':<{CONNECTION_BAR_WIDTH}}{' ' * SPACING}IDLE STATUS"
    )
    lines.append(f"{conn_bar}{' ' * SPACING}{idle_bar}")
    lines.append(divider)
    lines.append(f"Driver Side Engine Temperature: {ds18_str}")

    # Pass sensor min (-67F) and max (257F) to scale the bar accurately
    # (Or use custom operational limits like min_val=0, max_val=200 for better visual range)
    lines.append(
        progress_bar(driver_side_engine_bay_temperature, min_val=-67, max_val=257)
    )

    lines.append(f"LOAD: {load}%")
    lines.append(progress_bar(load))
    lines.append(f"THROTTLE: {throttle}%")
    lines.append(progress_bar(throttle))
    lines.append(divider)
    lines.append(f"PI Temperature: {pi_str}")
    lines.append(progress_bar(pi_cpu_temp))
    lines.append(f"CPU: {pi_cpu_usage}%")
    lines.append(progress_bar(pi_cpu_usage))
    lines.append(f"RAM: {pi_ram_usage}%")
    lines.append(progress_bar(pi_ram_usage))

    print_screen(lines)


def data_animation():
    """Sweep all bars from 0 to 100 and back"""
    steps = list(range(0, 101, 5)) + list(range(100, -1, -5))

    for value in steps:
        fake_store = {
            "Driver Side Engine Bay Temperature": value,
            "Engine Load": value,
            "Throttle Position": value,
            "PI CPU Temperature": value,
            "PI CPU Usage": value,
            "PI RAM Usage": value,
            "Idle Indicator": False,  # Demo state -- drives the loading-bar sweep
        }

        render_terminal(fake_store)
        time.sleep(0.07)
