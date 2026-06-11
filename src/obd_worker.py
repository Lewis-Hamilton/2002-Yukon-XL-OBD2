import time
from datetime import datetime
from gear_calc import estimate_gear
from idle_calc import idle_ready

def obd_worker(connection, all_data, data_store, data_lock, csv_queue):
    """
    OBD worker thread that queries sensors based on priority.
    
    Args:
        connection: The OBD connection object
        all_data: List of ObdData objects to query
        data_store: Shared dictionary to store sensor values
        csv_queue: Queue to send data to CSV logger
    """
    # Track when each sensor was last updated
    last_update_times = {data.name: 0 for data in all_data}
    last_csv_write = 0
    
    # Define update intervals for each priority (in seconds)
    priority_intervals = {
        "fast": 0.75,
        "medium": 2.5,
        "slow": 10.0
    }
        
    while True:
        try:
            current_time = time.time()
            local_updates = {}
            
            # Update sensors based on their priority
            for data in all_data:
                time_since_update = current_time - last_update_times[data.name]
                interval = priority_intervals.get(data.priority, None)
                
                if interval is not None and time_since_update >= interval:
                    val = data.response

                    if val is not None:
                        local_updates[data.name] = val
                        last_update_times[data.name] = current_time
                    else:
                        pass

            if local_updates:
                with data_lock:
                    data_store.update(local_updates)
            
            with data_lock:
                current_rpm = local_updates.get("RPM", data_store.get("RPM", 0))
                current_speed = local_updates.get("Speed", data_store.get("Speed", 0))
                current_load = local_updates.get("Engine Load", data_store.get("Engine Load", 0))

            if current_rpm is not None and current_speed is not None:
                calculated_gear = estimate_gear(current_rpm, current_speed, current_load)
                calculated_idle = idle_ready(current_rpm, current_speed)
                with data_lock:
                    data_store["Estimated Gear"] = calculated_gear
                    data_store["Idle Indicator"] = calculated_idle

            # Write to CSV every 1 second
            if current_time - last_csv_write >= 1.0:
                data_row = {"Time": datetime.now().time()}

                with data_lock:
                    for data in all_data:
                        data_row[f"{data.name} ({data.unit})"] = data_store.get(data.name, 0)
                
                csv_queue.put(data_row)  # Send to CSV thread
                last_csv_write = current_time
            
            time.sleep(0.05)  # Small sleep to prevent CPU hammering
            
        except Exception as e:
            print(f"OBD Thread Error: {e}")
            break

