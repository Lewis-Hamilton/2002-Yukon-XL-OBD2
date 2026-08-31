def get_ds18b20_temp_f(sensor_id: str) -> float | None:
    """
    Reads raw temperature from a DS18B20 sensor sysfs path and converts to Fahrenheit.
    Returns None if reading fails or CRC check fails.
    """
    sensor_path = f"/sys/bus/w1/devices/{sensor_id}/w1_slave"
    try:
        with open(sensor_path, "r") as f:
            lines = f.readlines()

        # Verify CRC check passed ('YES' at end of line 1)
        if not lines or not lines[0].strip().endswith("YES"):
            return None

        # Extract 't=XXXXX' value from line 2
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :].strip()
            temp_c = float(temp_string) / 1000.0
            return temp_c * 1.8 + 32.0
    except (FileNotFoundError, IndexError, ValueError):
        return None

    return None
