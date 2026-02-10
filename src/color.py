import time
import sys

# Define ANSI color codes as constants for readability
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_CYAN = "\033[96m" # For labels

def get_temp_color(temp_value):
    """Returns the ANSI color code based on temperature value."""
    if temp_value >= 220: # Example: Very hot
        return COLOR_RED
    elif temp_value >= 200: # Example: Getting warm
        return COLOR_YELLOW
    else: # Normal
        return COLOR_GREEN

def display_obd_data_with_color(connection):
    """
    Simulates querying and displaying OBD data with dynamic colors.
    Uses \r to overwrite the line.
    """
    # Dummy connection and data for demonstration
    # In your real code, you'd get actual connection and obd.commands
    # For now, let's use a mock-like structure
    class MockConnection:
        def is_connected(self): return True
        def query(self, cmd):
            # Simulate responses
            if cmd.name == "RPM": return MockResponse(1500 + time.time() % 500)
            if cmd.name == "SPEED": return MockResponse(30 + time.time() % 40)
            if cmd.name == "COOLANT_TEMP": return MockResponse(180 + (time.time() % 30))
            return MockResponse(None) # For unsupported or null responses

    class MockCommand:
        def __init__(self, name): self.name = name

    class MockResponse:
        def __init__(self, value): self.value = value
        def is_null(self): return self.value is None

    # Replace with your actual connection = obd.OBD()
    connection = MockConnection()

    # Replace with your actual commands
    commands_to_monitor = [
        MockCommand("RPM"),
        MockCommand("SPEED"),
        MockCommand("COOLANT_TEMP"),
    ]

    if not connection.is_connected():
        print("OBD connection not established.", COLOR_RESET)
        return

    print("Monitoring OBD Data (Ctrl+C to stop)...")
    print("-" * 50) # Separator line

    try:
        while True:
            data_parts = []
            for cmd in commands_to_monitor:
                response = connection.query(cmd)
                value = response.value if not response.is_null() else "N/A"

                if cmd.name == "COOLANT_TEMP" and isinstance(value, (int, float)):
                    color_code = get_temp_color(value)
                    data_parts.append(f"{COLOR_CYAN}{cmd.name}:{color_code}{value}°F{COLOR_RESET}")
                else:
                    data_parts.append(f"{COLOR_CYAN}{cmd.name}:{COLOR_GREEN}{value}{COLOR_RESET}")

            # Join parts and print on the same line, overwriting previous
            output_line = " | ".join(data_parts)
            print(f"\r{output_line.ljust(80)}", end="") # ljust to clear previous longer lines
            sys.stdout.flush()

            time.sleep(1) # Update every second

    except KeyboardInterrupt:
        print(f"\n{COLOR_RESET}Monitoring stopped.")
    finally:
        # connection.close() # Uncomment for real OBD connection
        pass # For mock connection

if __name__ == "__main__":
    display_obd_data_with_color(None) # Pass None as connection for this mock example