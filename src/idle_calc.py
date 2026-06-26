import time
from args import parser

args = parser.parse_args()

IDLE_DELAY = 20
STOP_DELAY = 5

_stopped_since = 0
_below_idle_since = None
_prev_speed = 0

def idle_ready(rpm, speed):
    global _stopped_since, _below_idle_since, _prev_speed

    if speed > 0:
        _stopped_since = None
        _below_idle_since = IDLE_DELAY
        _prev_speed = speed
        return True

    # speed == 0 from here on
    if _prev_speed is None or _prev_speed > 0:
        _stopped_since = time.time()

    _prev_speed = speed

    if time.time() - _stopped_since < STOP_DELAY:
        # waiting to slow down, don't check idle
        return True

    if rpm < args.idle_rpm:
        if _below_idle_since is None:
            _below_idle_since = time.time()
        return (time.time() - _below_idle_since) >= IDLE_DELAY
    else:
        _below_idle_since = None
        return False