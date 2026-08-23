def check_connection(connection):
    """Raises ConnectionError if the given connection isn't actually
    connected. Doesn't print or decide what happens next -- that's the
    caller's job (e.g. OBDConnector treats this as non-fatal).
    """
    if not connection.is_connected():
        raise ConnectionError(
            "Failed to connect to the OBD-II adapter. Make sure it's "
            "plugged in and your car's ignition is on."
        )
