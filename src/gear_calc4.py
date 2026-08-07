def estimate_gear4(current_speed, current_rpm, throttle_pct, last_gear):
    # 1. Below 5 MPH is Neutral / Park / Stopped
    if current_speed < 5:
        return "N/P"

    if current_speed == 0:
        return "---"

    ratio = current_rpm / current_speed

    # 2. Coasting Guard:
    # Only hold last_gear if throttle is 0% AND engine is near idle (~950 RPM),
    # UNLESS the calculated ratio clearly indicates a low gear (1st or 2nd ratio >= 45.0)
    if throttle_pct < 3 and current_rpm <= 950 and ratio < 45.0:
        if last_gear not in ("N/P", "---", None):
            return last_gear

    # 3. Ratio-based gear evaluation
    if ratio >= 85.0:
        return "1st"
    elif 45.0 <= ratio < 85.0:
        return "2nd"
    elif 37.0 <= ratio < 45.0:
        return "3rd"
    elif 0.0 < ratio < 37.0:
        return "4th (OD)"
    else:
        return "---"