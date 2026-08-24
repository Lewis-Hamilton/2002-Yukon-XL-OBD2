import sys


def start_check(is_switch_pressed_fn) -> None:
    """Checks the auto-start switch state.

    If disabled, prints status, flushes stdout, and terminates the script cleanly.
    """
    if is_switch_pressed_fn():
        print("Auto-start switch is active. Auto-start disabled. Exiting.")
        sys.stdout.flush()
        sys.exit(0)
