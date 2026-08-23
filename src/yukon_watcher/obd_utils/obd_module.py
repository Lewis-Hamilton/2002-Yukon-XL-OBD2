"""Single source of truth for which `obd` module (real vs. fake) is in
use. Anything that needs OBD command definitions or wants to open a
connection should import `obd` from here, instead of re-deriving it from
args in every file.

Also silences python-obd's own logging (e.g. "No OBD-II adapters
found", "Cannot load commands: No connection to car"). That library
logs those directly via its own handler rather than just raising, and
since OBDConnector retries continuously in the background, those lines
would otherwise print on every retry and corrupt the terminal's
fixed-layout redraw.
"""

import logging
import os

from yukon_watcher.args import parser

args = parser.parse_args()

if args.testing or args.manual_testing:
    import yukon_watcher.dev_utils.fake_obd as obd
    os.environ["GPIOZERO_PIN_FACTORY"] = "mock"
else:
    import obd

    # python-obd exposes its own logger for exactly this purpose; set
    # the underlying logger name directly too as a fallback in case the
    # `logger` attribute isn't present in some version.
    if hasattr(obd, "logger"):
        obd.logger.setLevel(logging.CRITICAL)
    logging.getLogger("obd").setLevel(logging.CRITICAL)

__all__ = ["obd"]
