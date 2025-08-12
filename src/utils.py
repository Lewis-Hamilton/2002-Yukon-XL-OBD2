# import obd
# from fake_obd import FakeOBD
import os

def check_connection(connection):
    if not connection.is_connected():
        print("Failed to connect to the OBD-II adapter. Make sure it's plugged in and your car's ignition is on.")
    else:
        print("Connected to OBD-II adapter!")

def get_filename(filename):
    """
    Checks if a file exists and returns a unique name by adding a number.
    
    Args:
        filename (str): The original filename (e.g., 'examplefile.csv').
    
    Returns:
        str: A unique filename (e.g., 'examplefile1.csv').
    """
    # Split the filename into the base and the extension
    base, extension = os.path.splitext(filename)
    counter = 1
    
    # Loop until a unique filename is found
    new_filename = filename
    while os.path.exists(new_filename):
        new_filename = f"{base}({counter}){extension}"
        counter += 1
        
    return new_filename

def celsius_to_fahrenheit(celsius):
  fahrenheit = (celsius * 9/5) + 32
  return fahrenheit

def convert_to_number(dirty_string):
    my_string = dirty_string
    cleaned_string = my_string.replace(" Celsius", "")
    cleaned_string = cleaned_string.strip()
    try:
        numeric_value = float(cleaned_string)
        return numeric_value
    except ValueError:
        print(f"Error: Could not convert '{cleaned_string}' to a number.")
        return None