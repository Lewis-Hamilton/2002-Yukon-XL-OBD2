import obd
import time

# Auto-connect to the OBD-II adapter.
# python-OBD will scan for available serial ports.
# If you know your COM port, you can specify it:
# connection = obd.OBD("COM3") # For Windows, replace COM3 with your port
# connection = obd.OBD("/dev/ttyUSB0") # For Linux/macOS

# 2002 yukon xl supported commands
# Available commands (supported by your car):
# - FUEL_STATUS
# - DTC_INTAKE_TEMP
# - DTC_O2_B1S1
# - SPEED
# - PIDS_A
# - DTC_ENGINE_LOAD
# - DTC_O2_B2S1
# - DTC_RPM
# - AUX_INPUT_STATUS
# - SHORT_FUEL_TRIM_2
# - DTC_O2_B1S2
# - ELM_VERSION
# - RPM
# - O2_B2S1
# - DTC_SHORT_FUEL_TRIM_2
# - COOLANT_TEMP
# - DTC_TIMING_ADVANCE
# - DTC_THROTTLE_POS
# - STATUS
# - INTAKE_PRESSURE
# - DTC_O2_SENSORS
# - DTC_OBD_COMPLIANCE
# - GET_CURRENT_DTC
# - LONG_FUEL_TRIM_2
# - DTC_INTAKE_PRESSURE
# - O2_B2S2
# - OBD_COMPLIANCE
# - DTC_FUEL_STATUS
# - PIDS_9A
# - DTC_STATUS
# - DTC_LONG_FUEL_TRIM_1
# - TIMING_ADVANCE
# - LONG_FUEL_TRIM_1
# - DTC_O2_B2S2
# - ELM_VOLTAGE
# - DTC_MAF
# - O2_B1S1
# - INTAKE_TEMP
# - MAF
# - MIDS_A
# - CLEAR_DTC
# - ENGINE_LOAD
# - DTC_AUX_INPUT_STATUS
# - O2_B1S2
# - SHORT_FUEL_TRIM_1
# - DTC_SPEED
# - THROTTLE_POS
# - O2_SENSORS
# - DTC_COOLANT_TEMP
# - DTC_LONG_FUEL_TRIM_2
# - GET_DTC
# - DTC_SHORT_FUEL_TRIM_1


# connection = obd.OBD()
# open env source env/bin/activate
connection = obd.OBD(portstr="/dev/ttyUSB0")

# Check if the connection was successful
if not connection.is_connected():
    print("Failed to connect to the OBD-II adapter. Make sure it's plugged in and your car's ignition is on.")
else:
    print("Connected to OBD-II adapter!")

    # For a 2002 Yukon XL, the protocol is likely SAE J1850 VPW.
    # python-OBD usually auto-detects, but if you have issues, you can try forcing it:
    # connection = obd.OBD(portstr="COM3", protocol="J1850VPW")

    print("\nAvailable commands (supported by your car):")
    # Get a list of commands supported by your vehicle
    supported_commands = connection.supported_commands
    for command in supported_commands:
        print(f"- {command.name}")

    print("\n--- Real-time Data ---")
    while True:
        try:
            # Example commands to query real-time data
            # You can find a full list of supported commands in the python-OBD documentation
            # Common ones include: RPM, SPEED, COOLANT_TEMP, MAF, THROTTLE_POS, FUEL_STATUS
            
            
            cmd_fuel = obd.commands.FUEL_STATUS
            cmd_speed = obd.commands.SPEED
            cmd_rpm = obd.commands.RPM
            cmd_coolant = obd.commands.COOLANT_TEMP
            cmd_voltage = obd.commands.ELM_VOLTAGE
            cmd_throttle = obd.commands.THROTTLE_POS
            # cmd_intake_temp = obd.commands.INTAKE_TEMP
            
            
            # cmd_rpm = obd.commands.RPM
            # cmd_speed = obd.commands.SPEED
            # cmd_coolant_temp = obd.commands.COOLANT_TEMP
            # cmd_maf = obd.commands.MAF
            # cmd_throttle_pos = obd.commands.THROTTLE_POS

            # response_rpm = connection.query(cmd_rpm)
            # response_speed = connection.query(cmd_speed)
            # response_coolant_temp = connection.query(cmd_coolant_temp)
            # response_maf = connection.query(cmd_maf)
            # response_throttle_pos = connection.query(cmd_throttle_pos)
            
            # response_intake_temp = connection.query(cmd_intake_temp)
            response_fuel = connection.query(cmd_fuel)
            response_speed = connection.query(cmd_speed)
            response_rpm = connection.query(cmd_rpm)
            response_coolant = connection.query(cmd_coolant)
            response_voltage = connection.query(cmd_voltage)
            response_throttle = connection.query(cmd_throttle)

            # rpm = response_rpm.value if response_rpm.is_successful() else "N/A"
            # speed = response_speed.value if response_speed.is_successful() else "N/A"
            # coolant_temp = response_coolant_temp.value if response_coolant_temp.is_successful() else "N/A"
            # maf = response_maf.value if response_maf.is_successful() else "N/A"
            # throttle_pos = response_throttle_pos.value if response_throttle_pos.is_successful() else "N/A"
            
            #intake_temp = response_intake_temp.value
            #idk = response_intake_temp

            # print(f"RPM: {rpm}")
            # print(f"Speed: {speed}")
            # print(f"Coolant Temp: {coolant_temp}")
            # print(f"MAF: {maf}")
            # print(f"Throttle Position: {throttle_pos}")
            # print("-" * 20)
            
            # print(f"{idk}")
            # print(f"Intake Temp: {intake_temp}")
            
            # print(f"Fuel Status: {response_fuel}")
            print(f"Speed: {response_speed}")
            print(f"Throttle Position: {response_throttle}")
            print(f"RPM: {response_rpm}")
            print(f"Coolant Temp: {response_coolant}")
            print(f"Elm Voltage: {response_voltage}")

            time.sleep(7) # Wait for 7 second before next query

        except KeyboardInterrupt:
            print("\nStopping real-time data acquisition.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5) # Wait before retrying