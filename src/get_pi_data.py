import psutil

def get_pi_cpu_usage():
    import psutil
    return psutil.cpu_percent(interval=None)

def get_pi_ram_usage():
    import psutil
    return psutil.virtual_memory().percent

def get_pi_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_milli_c = int(f.read().strip())
            temp_c = temp_milli_c / 1000.0
            return round(temp_c, 1)
    except Exception:
        return None