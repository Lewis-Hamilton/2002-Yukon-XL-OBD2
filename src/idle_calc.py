import time
from args import parser

args = parser.parse_args()

_below_idle_since = None
IDLE_DELAY = 15
STOP_DELAY = 5

_stopped_since = None
_below_idle_since = None

def idle_ready(rpm, speed):
    global _stopped_since, _below_idle_since

    if speed > 0:
        _stopped_since = None
        _below_idle_since = None
        return True

    if _stopped_since is None:
        _stopped_since = time.time()

    if time.time() - _stopped_since < STOP_DELAY:
        # waiting to slow down, don't check idle
        return False

    if rpm < args.idle_rpm:
        if _below_idle_since is None:
            _below_idle_since = time.time()
        return (time.time() - _below_idle_since) >= IDLE_DELAY
    else:
        _below_idle_since = None
        return False