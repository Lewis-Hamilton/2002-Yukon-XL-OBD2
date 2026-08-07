def estimate_gear4(current_speed, current_rpm, throttle_pct, last_gear):
    # 1. Below 5 MPH is Neutral / Park / Stopped
    if current_speed < 5:
        return "N/P"

    if current_speed == 0:
        return "---"

    ratio = current_rpm / current_speed

    # 2. Coasting Guard:
    # Hold last_gear if throttle is closed AND engine is near idle (~950 RPM),
    # UNLESS the ratio clearly indicates 1st gear (ratio >= 72.0)
    if throttle_pct < 3 and current_rpm <= 950 and ratio < 72.0:
        if last_gear not in ("N/P", "---", None):
            return last_gear

    # 3. Shift-Initiation Ratio Boundaries
    if ratio >= 72.0:
        return "1st"
    elif 52.0 <= ratio < 72.0:
        return "2nd"
    elif 35.0 <= ratio < 52.0:
        return "3rd"
    elif 0.0 < ratio < 35.0:
        return "4th (OD)"
    else:
        return "---"