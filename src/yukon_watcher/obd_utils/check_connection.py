def check_connection(connection):
    if not connection.is_connected():
        print(
            "Failed to connect to the OBD-II adapter. Make sure it's plugged in and your car's ignition is on."
        )
        raise ConnectionError("OBD-II connection failed")
    else:
        return
