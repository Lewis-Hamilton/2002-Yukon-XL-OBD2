def estimate_gear(rpm, speed):
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

# For now this will be all the ratios that are too low
# All of these gears should shift too early

    # GEARS = [
    #     Gear("1st", 130, 9999),
    #     Gear("2nd", 75, 129.99),
    #     Gear("3rd", 35, 74.99),
    #     Gear("4th (OD)", 0, 34.99),
    # ]

# lower ratio based on gemini suggustion in file2
    # GEARS = [
    #     Gear("1st", 80, 9999),
    #     Gear("2nd", 40, 79.99),
    #     Gear("3rd", 25, 39.99),
    #     Gear("4th (OD)", 0, 24.99),
    # ]

    
    # new gemini suggustion
    GEARS = [
        Gear("1st", 85.0, 9999.0),
        Gear("2nd", 45.0, 84.99),
        Gear("3rd", 37.0, 44.99),
        Gear("4th (OD)", 0.0, 36.99),
    ]

    # get rid of "OD" in the 4th name, stupid

    for gear in GEARS:
        if gear.min <= rounded_ratio <= gear.max:
            return gear.name
    return "---"