"""Shared, live view of the OBD connection -- the single source of
truth for whether OBD is currently usable.

Importantly, this does NOT rely on the adapter's own `is_connected()`
being trustworthy. Many adapters draw power from the always-hot battery
pin on the OBD port and stay link-connected even with the vehicle fully
off -- it's the ECU that goes quiet, not the adapter. So instead we
track when a PID query last actually succeeded (`last_success_time`);
OBDConnector's watchdog uses that staleness, not the adapter's self-
reported status, to decide the car has gone quiet.
"""

import time

connection = None
is_connected = False
last_error = None
last_success_time = None


def set_connected(new_connection):
    global connection, is_connected, last_error, last_success_time
    connection = new_connection
    is_connected = True
    last_error = None
    last_success_time = time.time()


def set_disconnected(error=None):
    global connection, is_connected, last_error, last_success_time
    connection = None
    is_connected = False
    last_success_time = None
    if error is not None:
        last_error = error


def record_success():
    """Call whenever a PID query actually returns real, parseable
    data. This is the signal OBDConnector's watchdog uses -- if it's
    been too long since the last one, the car is treated as gone even
    if the adapter link itself still claims to be up.
    """
    global last_success_time
    last_success_time = time.time()


def is_stale(timeout: float) -> bool:
    if last_success_time is None:
        return True
    return (time.time() - last_success_time) > timeout
