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

# Ratios Tested
# 41 is too low for 3rd gear min, switched to 42
# 95 is too low for 1st gear min, switched to 110
# 110 is also too low for 1st gear min, switched to 120
# Correct 4th max is 41.99 but going radical now to try stuff
# I think 41.99 is too high for max 4th gear, trying 34.99
# correct 2nd min is 69 but going radical to try stuff

    GEARS = [
        Gear("1st", 125, 9999),
        Gear("2nd", 73, 124.99),
        Gear("3rd", 35, 72.99),
        Gear("4th (OD)", 0, 34.99),
    ]

    # get rid of "OD" in the 4th name, stupid

    for gear in GEARS:
        if gear.min <= rounded_ratio <= gear.max:
            return gear.name
    return "---"