import os

from yukon_watcher.args import parser
from yukon_watcher.display_outputs.startup_screen import startup_screen
from yukon_watcher.display_outputs.stereo_screen import hide_cursor
from yukon_watcher.obd_utils.connection import OBDConnector
from yukon_watcher.runtime import run

args = parser.parse_args()

if args.testing or args.manual_testing:
    import yukon_watcher.dev_utils.fake_obd as obd
else:
    import obd


def main():
    os.system("clear")
    hide_cursor()

    connector = OBDConnector(obd, use_fake=args.testing or args.manual_testing)
    connect_thread = connector.start()

    # Play animation while connection happens in the background
    startup_screen(connect_thread)
    connector.raise_if_failed()

    run(connector, args)


if __name__ == "__main__":
    main()
