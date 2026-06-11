# from args import parser

# args = parser.parse_args()

# def idle_ready(rpm, speed):
#     if speed > 0 or rpm < args.idle_rpm:
#         return True
#     elif rpm >= args.idle_rpm and speed == 0:
#         return False

import time
from args import parser

args = parser.parse_args()

_below_idle_since = None
IDLE_DELAY = 15

def idle_ready(rpm, speed):
    global _below_idle_since

    if speed > 0:
        _below_idle_since = None
        return True

    if rpm < args.idle_rpm:
        if _below_idle_since is None:
            _below_idle_since = time.time()
        return (time.time() - _below_idle_since) >= IDLE_DELAY
    else:
        _below_idle_since = None
        return False