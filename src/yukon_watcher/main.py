import os
import signal

from yukon_watcher.args import parser
from yukon_watcher.display_outputs.startup_screen import startup_screen
from yukon_watcher.display_outputs.stereo_screen import hide_cursor, show_cursor
from yukon_watcher.obd_utils.connection import OBDConnector
from yukon_watcher.obd_utils.obd_module import obd
from yukon_watcher.runtime import run

args = parser.parse_args()


def _handle_sigterm(signum, frame):
    """`systemctl stop yukon.service` (including from the GPIO
    shutdown button's power-off callback) sends SIGTERM, which Python
    terminates on immediately by default -- no `finally` blocks run, no
    cleanup happens. Converting it into a KeyboardInterrupt routes it
    through the same graceful-shutdown path as Ctrl+C, so run()'s
    `finally` (CSV flush, OBD close, cursor) still runs
    before the process actually exits -- which matters here since the
    shutdown button's `poweroff` call waits for `systemctl stop` to
    finish first.
    """
    raise KeyboardInterrupt


def main():
    os.system("clear")
    hide_cursor()
    signal.signal(signal.SIGTERM, _handle_sigterm)

    # Starts connecting in the background and keeps retrying/monitoring
    # for the rest of the run -- we never wait on it.
    connector = OBDConnector(obd, use_fake=args.testing or args.manual_testing)
    connector.start()

    try:
        startup_screen()  # Just the intro animation, not gated on OBD

        # Runs immediately either way: OBD gauges hold default values
        # until (re)connected; Pi data and CSV logging always run. If
        # OBD connects or drops out mid-run, my_data/obd_worker/
        # connection pick it up on their own, and the connection bar in
        # render_terminal reflects it -- no status print here, since
        # that could interleave with the terminal's fixed-layout redraw.
        run(connector, args)
    except KeyboardInterrupt:
        # Only reachable if SIGTERM/Ctrl+C landed during startup_screen(),
        # before run()'s own try/finally was active -- run() handles its
        # own KeyboardInterrupt and cleanup internally otherwise.
        print("\nStopping...")
        show_cursor()
        connector.close()


if __name__ == "__main__":
    main()
