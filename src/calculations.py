def estimate_gear(rpm, speed, engine_load=None):
    """
    Estimate current gear based on RPM and speed.
    
    Args:
        rpm: Current engine RPM
        speed: Current speed in MPH
        engine_load: Optional engine load percentage (for future refinement)
    
    Returns:
        str: Estimated gear ("1st", "2nd", "3rd", "4th (OD)", "N/P", or "---")
    """
    # Vehicle specifications for 2002 Yukon XL
    AXLE_RATIO = 3.73
    TIRE_DIAMETER = 31.1  # inches
    CONSTANT = 336.13
    
    # Transmission gear ratios (4L60E/4L65E typical for this vehicle)
    # Gear 1: 3.06
    # Gear 2: 1.63
    # Gear 3: 1.00
    # Gear 4: 0.70 (overdrive)
    
    # Calculate theoretical RPM per MPH for each gear
    RPM_PER_MPH_1ST = (AXLE_RATIO * 3.06 * CONSTANT) / TIRE_DIAMETER  # ~123
    RPM_PER_MPH_2ND = (AXLE_RATIO * 1.63 * CONSTANT) / TIRE_DIAMETER  # ~65
    RPM_PER_MPH_3RD = (AXLE_RATIO * 1.00 * CONSTANT) / TIRE_DIAMETER  # ~40
    RPM_PER_MPH_4TH = (AXLE_RATIO * 0.70 * CONSTANT) / TIRE_DIAMETER  # ~28
    
    # Handle edge cases
    if speed < 5:
        return "N/P"  # Neutral/Park or too slow to determine
    
    if rpm == 0:
        return "---"  # No RPM data
    
    # Calculate current ratio (RPM per MPH)
    current_ratio = rpm / speed
    
    # Determine gear using midpoints between theoretical ratios
    # Midpoint between 1st and 2nd: (123 + 65) / 2 = 94
    # Midpoint between 2nd and 3rd: (65 + 40) / 2 = 52.5
    # Midpoint between 3rd and 4th: (40 + 28) / 2 = 34
    
    if current_ratio > 90:
        return "1st"
    elif 52 < current_ratio <= 90:
        return "2nd"
    elif 34 < current_ratio <= 52:
        return "3rd"
    elif current_ratio <= 34:
        return "4th (OD)"
    else:
        return "---"  # Shouldn't reach here, but safety fallback