import logging
import threading

from yukon_watcher.obd_utils.check_connection import check_connection

logger = logging.getLogger(__name__)


class OBDConnector:
    """Owns the lifecycle of the OBD connection: connecting in the
    background, exposing the result, and closing it down cleanly.
    """

    def __init__(self, obd_module, use_fake: bool):
        self.obd_module = obd_module
        self.use_fake = use_fake
        self.connection = None
        self.error = None
        self._thread = threading.Thread(target=self._connect, daemon=True)

    def start(self) -> threading.Thread:
        """Kick off the connection attempt in the background and return
        the thread so callers can wait on it (e.g. during a startup
        animation).
        """
        self._thread.start()
        return self._thread

    def _connect(self):
        try:
            self.connection = (
                self.obd_module.FakeOBD() if self.use_fake else self.obd_module.OBD()
            )
            check_connection(self.connection)
        except Exception as e:  # noqa: BLE001
            self.error = e

    def raise_if_failed(self):
        """Call after the connect thread has finished. Raises whatever
        went wrong, or ConnectionError if we never got a connection.
        """
        if self.error:
            raise self.error
        if self.connection is None:
            raise ConnectionError("OBD connection timed out")

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception as err:  # noqa: BLE001
                logger.warning(f"Error while closing OBD connection: {err}")
