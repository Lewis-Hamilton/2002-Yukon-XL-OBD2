import logging
import threading
import time

from yukon_watcher.obd_utils import obd_state
from yukon_watcher.obd_utils.check_connection import check_connection

logger = logging.getLogger(__name__)

RETRY_INTERVAL = 5.0  # seconds between reconnect attempts while offline
STALE_TIMEOUT = 5.0  # seconds without a successful PID read before we
# treat the car as gone, even if the adapter link claims to be up
POLL_INTERVAL = 1.0  # how often to check staleness (cheap, so frequent)


class OBDConnector:
    """Owns the OBD connection for the life of the app.

    Runs a persistent background thread that connects immediately, then
    keeps watching in two ways:
      1. If nothing has connected yet (or a reconnect attempt is due),
         it tries to (re)connect, throttled to `retry_interval` so it
         doesn't hammer the port.
      2. If `obd_state` says connected but no PID has actually
         succeeded in `stale_timeout` seconds, it's marked disconnected
         -- this is what catches "engine/accessory off" even when the
         adapter's own link-level connection never reports a drop.

    Callers never need to wait on this -- `connected` / `error` just
    reflect the current state, and the rest of the app (my_data/
    obd_worker) already treats "not connected" as "use defaults".
    """

    def __init__(
        self,
        obd_module,
        use_fake: bool,
        retry_interval: float = RETRY_INTERVAL,
        stale_timeout: float = STALE_TIMEOUT,
        poll_interval: float = POLL_INTERVAL,
    ):
        self.obd_module = obd_module
        self.use_fake = use_fake
        self.retry_interval = retry_interval
        self.stale_timeout = stale_timeout
        self.poll_interval = poll_interval
        self._last_attempt = 0.0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)

    @property
    def connected(self) -> bool:
        return obd_state.is_connected

    @property
    def error(self):
        return obd_state.last_error

    def start(self) -> threading.Thread:
        """Starts the persistent connect/reconnect/staleness thread and
        returns immediately -- this does NOT wait for a connection.
        """
        self._thread.start()
        return self._thread

    def _watch_loop(self):
        self._try_connect(force=True)
        while not self._stop.is_set():
            if obd_state.is_connected and obd_state.is_stale(self.stale_timeout):
                obd_state.set_disconnected()

            if not obd_state.is_connected:
                self._try_connect()

            self._stop.wait(self.poll_interval)

    def _try_connect(self, force: bool = False):
        now = time.time()
        if not force and (now - self._last_attempt) < self.retry_interval:
            return
        self._last_attempt = now

        try:
            connection = (
                self.obd_module.FakeOBD() if self.use_fake else self.obd_module.OBD()
            )
            check_connection(connection)
        except Exception as e:  # noqa: BLE001
            obd_state.set_disconnected(error=e)
            return

        obd_state.set_connected(connection)

    def stop(self):
        self._stop.set()

    def close(self):
        self.stop()
        connection = obd_state.connection
        if connection:
            try:
                connection.close()
            except Exception as err:  # noqa: BLE001
                logger.warning(f"Error while closing OBD connection: {err}")
        obd_state.set_disconnected()
