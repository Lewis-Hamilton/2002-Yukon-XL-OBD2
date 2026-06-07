import csv
import queue
from datetime import datetime
from utils import get_filename, create_logging_dir

def csv_logger(csv_queue, all_data, args):
    """
    Separate thread that writes data to CSV.
    
    Args:
        csv_queue: Queue to receive data from OBD worker
        all_data: List of ObdData objects (for column names)
        args: Command line arguments (for testing mode)
    """
    create_logging_dir()
    
    now = datetime.now()
    current_date = now.date()
    
    if args.testing == True:
        initial_csv_name = f"./logged_data/test-data-{current_date}.csv"
    else:
        initial_csv_name = f"./logged_data/{current_date}.csv"
    
    csv_name = get_filename(initial_csv_name)
    column_names = [f"{data.name} ({data.unit})" for data in all_data]
    column_names.insert(0, "Time")
    
    with open(csv_name, "w", newline="") as csvfile:
        thewriter = csv.DictWriter(csvfile, fieldnames=column_names)
        thewriter.writeheader()
        print(f"Logging data to '{csv_name}'...")
        
        while True:
            try:
                # Wait for data from the queue (blocks until data available)
                data_row = csv_queue.get(timeout=1)
                
                if data_row is None:  # Poison pill to stop the thread
                    print("CSV logger stopping...")
                    break
                
                thewriter.writerow(data_row)
                csvfile.flush()  # Make sure it's written to disk immediately
                
            except queue.Empty:
                # No data in queue, just continue
                continue
            except Exception as e:
                print(f"CSV Thread Error: {e}")
                time.sleep(1)