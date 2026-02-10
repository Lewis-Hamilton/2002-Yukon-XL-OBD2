import obd
from src.utils import check_connection

connection = obd.OBD(portstr="/dev/ttyUSB0")

check_connection(connection)



print("\nAvailable commands (supported by your car):")
# Get a list of commands supported by your vehicle
supported_commands = connection.supported_commands
for command in supported_commands:
    print(f"- {command.name}")