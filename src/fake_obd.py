# src/fake_obd.py

import time
import random

# --- Mimic obd.OBDCommand ---
class FakeOBDCommand:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<FakeOBDCommand: {self.name}>"

# --- Mimic obd.OBDResponse ---
class FakeOBDResponse:
    def __init__(self, value, is_null=False):
        self.value = value
        self._is_null = is_null

    def is_null(self):
        return self._is_null

    def __repr__(self):
        if self._is_null:
            return f"<FakeOBDResponse: NULL>"
        return f"<FakeOBDResponse: {self.value}>"

# --- Mimic obd.commands ---
class FakeOBDCommands:
    AUX_INPUT_STATUS = FakeOBDCommand("AUX_INPUT_STATUS")
    COOLANT_TEMP = FakeOBDCommand("COOLANT_TEMP")
    ENGINE_LOAD = FakeOBDCommand("ENGINE_LOAD")
    FUEL_STATUS = FakeOBDCommand("FUEL_STATUS")
    INTAKE_PRESSURE = FakeOBDCommand("INTAKE_PRESSURE")
    INTAKE_TEMP = FakeOBDCommand("INTAKE_TEMP")
    LONG_FUEL_TRIM_1 = FakeOBDCommand("LONG_FUEL_TRIM_1")
    LONG_FUEL_TRIM_2 = FakeOBDCommand("LONG_FUEL_TRIM_2")
    MAF = FakeOBDCommand("MAF")
    MIDS_A = FakeOBDCommand("MIDS_A")
    O2_B1S1 = FakeOBDCommand("O2_B1S1")
    O2_B1S2 = FakeOBDCommand("O2_B1S2")
    O2_B2S1 = FakeOBDCommand("O2_B2S1")
    O2_B2S2 = FakeOBDCommand("O2_B2S2")
    O2_SENSORS = FakeOBDCommand("O2_SENSORS")
    OBD_COMPLIANCE = FakeOBDCommand("OBD_COMPLIANCE")
    PIDS_9A = FakeOBDCommand("PIDS_9A")
    PIDS_A = FakeOBDCommand("PIDS_A")
    RPM = FakeOBDCommand("RPM")
    SHORT_FUEL_TRIM_1 = FakeOBDCommand("SHORT_FUEL_TRIM_1")
    SHORT_FUEL_TRIM_2 = FakeOBDCommand("SHORT_FUEL_TRIM_2")
    SPEED = FakeOBDCommand("SPEED")
    STATUS = FakeOBDCommand("STATUS")
    THROTTLE_POS = FakeOBDCommand("THROTTLE_POS")
    TIMING_ADVANCE = FakeOBDCommand("TIMING_ADVANCE")
    ELM_VERSION = FakeOBDCommand("ELM_VERSION")
    ELM_VOLTAGE = FakeOBDCommand("ELM_VOLTAGE")
    
commands = FakeOBDCommands()

# --- Mimic obd.OBD (the connection class) ---
class FakeOBD:
    def __init__(self, portstr=None, baudrate=None):
        print(f"FakeOBD: Initializing connection on port {portstr}...")
        self._is_connected = True
        self.portstr = portstr

    def is_connected(self):
        return self._is_connected

    def close(self):
        print("FakeOBD: Connection closed.")
        self._is_connected = False

    def query(self, command, force=False):
        if not self._is_connected:
            return FakeOBDResponse(None, is_null=True)

        print(f"FakeOBD: Querying {command.name}...", end="\r")

        # Simulate different responses for different commands
        if command.name == "RPM":
            num = random.uniform(600, 7000)
            decimals = random.choice([1, 2])
            rpm = round(num, decimals)
            return FakeOBDResponse(f"{rpm} revolutions_per_minute")
        elif command.name == "SPEED":
            return FakeOBDResponse(f"{random.randint(0, 160)}.0 kilometer_per_hour")
        elif command.name == "COOLANT_TEMP":
            # Simulate a Celsius value, as per your my_data.py
            return FakeOBDResponse(round(random.uniform(80.0, 105.0), 1))
        elif command.name == "ELM_VOLTAGE":
            return FakeOBDResponse(round(random.uniform(11.5, 14.5), 2))
        elif command.name == "THROTTLE_POS":
            return FakeOBDResponse(round(random.uniform(0.0, 99.9), 1))
        elif command.name == "INTAKE_TEMP":
            return FakeOBDResponse(round(random.uniform(20.0, 50.0), 1))
        elif command.name == "ENGINE_LOAD":
            return FakeOBDResponse(round(random.uniform(10.0, 80.0), 1))
        elif command.name == "AUX_INPUT_STATUS":
            return FakeOBDResponse(random.choice([0, 1]))
        elif command.name in ["O2_B1S1", "O2_B1S2", "O2_B2S1", "O2_B2S2"]:
            return FakeOBDResponse(round(random.uniform(0.1, 0.9), 2))
        elif command.name == "O2_SENSORS":
            return FakeOBDResponse("B1S1, B1S2, B2S1, B2S2")
        elif command.name == "TIMING_ADVANCE":
            return FakeOBDResponse(round(random.uniform(-15.0, 25.0), 1))
        elif command.name == "ELM_VERSION":
            return FakeOBDResponse("ELM327 v1.5 (Fake)")
        elif command.name == "MAF":
            return FakeOBDResponse(round(random.uniform(2.0, 200.0), 2))
        elif command.name == "INTAKE_PRESSURE":
            return FakeOBDResponse(random.randint(20, 100))
        elif command.name in ["SHORT_FUEL_TRIM_1", "SHORT_FUEL_TRIM_2"]:
            return FakeOBDResponse(round(random.uniform(-10.0, 10.0), 2))
        elif command.name in ["LONG_FUEL_TRIM_1", "LONG_FUEL_TRIM_2"]:
            return FakeOBDResponse(round(random.uniform(-5.0, 5.0), 2))
        elif command.name == "FUEL_STATUS":
            statuses = ["Closed loop", "Open loop"]
            return FakeOBDResponse(random.choice(statuses))
        elif command.name == "STATUS":
            return FakeOBDResponse("Monitor Status")
        elif command.name in ["PIDS_A", "PIDS_9A", "MIDS_A"]:
            return FakeOBDResponse("Supported")
        elif command.name == "OBD_COMPLIANCE":
            return FakeOBDResponse("EOBD")

        print(f"FakeOBD: No specific fake data for {command.name}. Returning null.")
        return FakeOBDResponse(None, is_null=True)

class FakeOBDStatus:
    CAR_CONNECTED = "CAR_CONNECTED"
    ELM_CONNECTED = "ELM_CONNECTED"
    NOT_CONNECTED = "NOT_CONNECTED"

OBDStatus = FakeOBDStatus()

class FakeLogger:
    def info(self, msg): print(f"[FAKE_OBD INFO] {msg}")
    def warning(self, msg): print(f"[FAKE_OBD WARNING] {msg}")
    def error(self, msg): print(f"[FAKE_OBD ERROR] {msg}")
    def debug(self, msg): print(f"[FAKE_OBD DEBUG] {msg}")
    def setLevel(self, level): pass

logger = FakeLogger()