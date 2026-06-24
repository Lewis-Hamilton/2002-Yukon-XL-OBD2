def estimate_gear2(rpm, speed):
    """
    Estimate current gear based on RPM and speed.
    
    Args:
        rpm: Current engine RPM
        speed: Current speed in MPH
    
    Returns:
        str: Estimated gear ("1st", "2nd", "3rd", "4th (OD)", "N/P", or "---")
    """

    # Handle edge cases
    if speed < 1:
        return "N/P"  # Neutral/Park or too slow to determine

    if rpm == 0:
        return "---"  # No RPM data

    # Calculate current ratio (RPM per MPH)
    current_ratio = rpm / speed
    if current_ratio != 0:
        rounded_ratio = round(current_ratio, 2)
    else:
        rounded_ratio = 0

    class Gear:
        def __init__(self, name, min, max):
            self.name = name
            self.min = min
            self.max = max

    GEARS = [
        Gear("1st", 95, 9999),
        Gear("2nd", 69, 94),
        Gear("3rd", 41, 68),
        Gear("4th (OD)", 0, 40),
    ]

    # get rid of "OD" in the 4th name, stupid

    for gear in GEARS:
        if gear.min <= rounded_ratio <= gear.max:
            return gear.name
    return "---"