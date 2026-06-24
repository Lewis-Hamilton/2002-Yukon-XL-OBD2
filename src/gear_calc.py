def estimate_gear(rpm, speed):
    """
    Estimate current gear based on RPM and speed.
    
    Args:
        rpm: Current engine RPM
        speed: Current speed in MPH
        engine_load: Optional engine load percentage (for future refinement)
    
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

    # Determine gear using midpoints between theoretical ratios
    # Midpoint between 1st and 2nd: (123 + 65) / 2 = 94
    # Midpoint between 2nd and 3rd: (65 + 40) / 2 = 52.5
    # Midpoint between 3rd and 4th: (40 + 28) / 2 = 34
    MIDPOINT_1ST_2ND = 90
    MIDPOINT_2ND_3RD = 52
    MIDPOINT_3RD_4TH = 34

    if current_ratio > MIDPOINT_1ST_2ND:
        return "1st"
    elif MIDPOINT_2ND_3RD < current_ratio <= MIDPOINT_1ST_2ND:
        return "2nd"
    elif MIDPOINT_3RD_4TH < current_ratio <= MIDPOINT_2ND_3RD:
        return "3rd"
    elif current_ratio <= MIDPOINT_3RD_4TH:
        return "4th (OD)"
    else:
        return "---"  # Shouldn't reach here, but safety fallback