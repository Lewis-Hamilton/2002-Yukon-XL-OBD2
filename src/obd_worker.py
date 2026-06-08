import time
from datetime import datetime
from gear_calc import estimate_gear
from get_pi_data import get_pi_stats, get_pi_cpu_temp

def obd_worker(connection, all_data, data_store, csv_queue):
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
        "fast": 0.5,    # Update twice per second
        "medium": 2.0,  # Update every 2 seconds
        "slow": 10.0    # Update every 10 seconds
    }
    
    print("OBD worker thread started")
    
    while True:
        try:
            current_time = time.time()
            
            # Update sensors based on their priority
            for data in all_data:
                time_since_update = current_time - last_update_times[data.name]
                interval = priority_intervals.get(data.priority, None)
                
                if interval is None:
                    continue
                # Should we update this sensor now?
                elif time_since_update >= interval:
                    val = data.response  # Query the car
                    data_store[data.name] = val
                    last_update_times[data.name] = current_time
            
            # Write to CSV every 1 second
            if current_time - last_csv_write >= 1.0:
                data_row = {"Time": datetime.now().time()}
                
                for data in all_data:
                    data_row[f"{data.name} ({data.unit})"] = data_store.get(data.name, 0)
                
                csv_queue.put(data_row)  # Send to CSV thread
                last_csv_write = current_time
            
            time.sleep(0.05)  # Small sleep to prevent CPU hammering
            
        except Exception as e:
            print(f"OBD Thread Error: {e}")
            time.sleep(1)

        data_store["Estimated Gear"] = estimate_gear(
        data_store.get("RPM", 0),
        data_store.get("Speed", 0),
        data_store.get("Engine Load", 0)
)

        cpu_usage, ram_usage = get_pi_stats()
        data_store["PI CPU Temperature"] = get_pi_cpu_temp()
        data_store["PI CPU Usage"] = cpu_usage
        data_store["PI RAM Usage"] = ram_usage