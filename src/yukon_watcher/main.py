import os

from yukon_watcher.args import parser
from yukon_watcher.display_outputs.startup_screen import startup_screen
from yukon_watcher.display_outputs.stereo_screen import hide_cursor
from yukon_watcher.obd_utils.connection import OBDConnector
from yukon_watcher.obd_utils.obd_module import obd
from yukon_watcher.runtime import run
from yukon_watcher.pi_utils.my_gpio import HardwareManager

args = parser.parse_args()


def main():
    os.system("clear")
    hide_cursor()
    hardware_manager = HardwareManager()

    # Starts connecting in the background and keeps retrying/monitoring
    # for the rest of the run -- we never wait on it.
    connector = OBDConnector(obd, use_fake=args.testing or args.manual_testing)
    connector.start()

    startup_screen()  # Just the intro animation, not gated on OBD

    # Runs immediately either way: OBD gauges hold default values until
    # (re)connected; Pi data and CSV logging always run. If OBD connects
    # or drops out mid-run, my_data/obd_worker/connection pick it up on
    # their own, and the connection bar in render_terminal reflects it --
    # no status print here, since that could interleave with the
    # terminal's fixed-layout redraw.
    run(connector, args)


if __name__ == "__main__":
    main()
