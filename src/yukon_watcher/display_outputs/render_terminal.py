import time

from yukon_watcher.display_outputs.stereo_screen import print_screen
from yukon_watcher.obd_utils import obd_state

BAR_WIDTH = 54
CONNECTION_BAR_WIDTH = 12  # Small and deliberate -- not a full-width gauge


def loading_bar():
    BLOCK_WIDTH = 20
    BAR_SPEED = 30
    travel = BAR_WIDTH - BLOCK_WIDTH
    period = travel * 2
    position = int(time.time() * BAR_SPEED) % period
    if position >= travel:
        position = period - position
    return (
        "\u2591" * position
        + "\u2588" * BLOCK_WIDTH
        + "\u2591" * (BAR_WIDTH - BLOCK_WIDTH - position)
    )


def idle_indicator(idle_status):
    if idle_status is None:
        # No OBD data to base this on -- blank, not "not idle"
        return "\u2591" * BAR_WIDTH
    if idle_status:
        return "\u2588" * BAR_WIDTH
    return loading_bar()


def connection_indicator(is_connected):
    """Solid when OBD is connected, empty when it isn't. No text, no
    error messages -- just a steady status bar that can't corrupt the
    fixed gauge layout the way a stray print() would.
    """
    if is_connected:
        return "\u2588" * CONNECTION_BAR_WIDTH
    return "\u2591" * CONNECTION_BAR_WIDTH


def progress_bar(bar_data):
    bar_fill = int((min(bar_data, 100) / 100) * BAR_WIDTH)
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
    idle_bar = idle_indicator(idle_status)

    # Pi temp status
    if pi_cpu_temp is None:
        pi_str = "--C"
    else:
        pi_str = f"{pi_cpu_temp}C"

    divider = "━" * BAR_WIDTH

    lines = []
    lines.append("Idle Status")
    lines.append(idle_bar)
    lines.append(divider)
    lines.append("OBD CONNECTION")
    lines.append(connection_indicator(obd_state.is_connected))
    lines.append(divider)
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
            "Engine Load": value,
            "Throttle Position": value,
            "PI CPU Temperature": value,
            "PI CPU Usage": value,
            "PI RAM Usage": value,
            "Idle Indicator": False,  # Demo state -- drives the loading-bar sweep
        }

        render_terminal(fake_store)
        time.sleep(0.07)
