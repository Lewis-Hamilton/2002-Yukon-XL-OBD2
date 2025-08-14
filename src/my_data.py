from args import parser

args = parser.parse_args()

if args.testing == True:
    import fake_obd as obd
    connection = obd.FakeOBD()

else:
    import obd
    connection = obd.OBD(portstr="/dev/ttyUSB0")


class ObdData:
    def __init__(self, name, cmd, unit):
        self.name = name
        self.cmd = cmd
        self.unit = unit
    
    @property 
    def response(self):
        myresponse = connection.query(self.cmd)
        return myresponse

AUX_INPUT_STATUS = ObdData(
    name="Auxillary Input",
    cmd=obd.commands.AUX_INPUT_STATUS,
    unit="Unkown"
)

COOLANT_TEMP = ObdData(
    name="Coolant Tempurature",
    cmd=obd.commands.COOLANT_TEMP,
    unit="Celsius"
)

ENGINE_LOAD = ObdData(
    name="Engine Load",
    cmd=obd.commands.ENGINE_LOAD,
    unit=" Percentage"
)

FUEL_STATUS = ObdData(
    name="Fuel Status",
    cmd=obd.commands.FUEL_STATUS,
    unit="Unkown"
)

INTAKE_PRESSURE = ObdData(
    name="Intake Pressure",
    cmd=obd.commands.INTAKE_PRESSURE,
    unit="kilopascal"
)

INTAKE_TEMP = ObdData(
    name="Intake Tempurature",
    cmd=obd.commands.INTAKE_TEMP,
    unit="Celsius"
)

LONG_FUEL_TRIM_1 = ObdData(
    name="Bank 1 Long Fuel Trim",
    cmd=obd.commands.LONG_FUEL_TRIM_1,
    unit="Percentage"
)

LONG_FUEL_TRIM_2 = ObdData(
    name="Bank 2 Long Fuel Trim",
    cmd=obd.commands.LONG_FUEL_TRIM_2,
    unit="Percentage"
)

MAF = ObdData(
    name="Mass Airflow Sensor",
    cmd=obd.commands.MAF,
    unit="Unkown"
)

MIDS_A = ObdData(
    name="MIDS A",
    cmd=obd.commands.MIDS_A,
    unit="Unkown"
)

O2_B1S1 = ObdData(
    name="O2 Bank 1 Sensor 1",
    cmd=obd.commands.O2_B1S1,
    unit="Volts"
)

O2_B1S2 = ObdData(
    name="O2 Bank 1 Sensor 2",
    cmd=obd.commands.O2_B1S2,
    unit="Volts"
)

O2_B2S1 = ObdData(
    name="O2 Bank 2 Sensor 1",
    cmd=obd.commands.O2_B2S1,
    unit="Volts"
)

O2_B2S2 = ObdData(
    name="O2 Bank 2 Sensor 2",
    cmd=obd.commands.O2_B2S2,
    unit="Volts"
)

O2_SENSORS = ObdData(
    name="O2 Sensors Status",
    cmd=obd.commands.O2_SENSORS,
    unit="Unkown"
)

OBD_COMPLIANCE = ObdData(
    name="OBD Compliance",
    cmd=obd.commands.OBD_COMPLIANCE,
    unit="Unkown"
)

PIDS_9A = ObdData(
    name="PIDS 9A",
    cmd=obd.commands.PIDS_9A,
    unit="Unkown"
)

PIDS_A = ObdData(
    name="PIDS A",
    cmd=obd.commands.PIDS_A,
    unit="Unkown"
)

RPM = ObdData(
    name="RPM",
    cmd=obd.commands.RPM,
    unit="RPM"
)

SHORT_FUEL_TRIM_1 = ObdData(
    name="Bank 1 Short Fuel Trim",
    cmd=obd.commands.SHORT_FUEL_TRIM_1,
    unit="Unkown"
)

SHORT_FUEL_TRIM_2 = ObdData(
    name="Bank 2 Short Fuel Trim",
    cmd=obd.commands.SHORT_FUEL_TRIM_2,
    unit="Unkown"
)

SPEED = ObdData(
    name="Speed",
    cmd=obd.commands.SPEED,
    unit="Kilometers"
)

STATUS = ObdData(
    name="OBD Status",
    cmd=obd.commands.STATUS,
    unit="Unkown"
)

THROTTLE_POSITION = ObdData(
    name="Throttle Position",
    cmd=obd.commands.THROTTLE_POS,
    unit="Unkown"
)

TIMING_ADVANCE = ObdData(
    name="Timing Advance",
    cmd=obd.commands.TIMING_ADVANCE,
    unit="Degrees"
)
# maybe display this on startup
VERSION = ObdData(
    name="Firmware Version",
    cmd=obd.commands.ELM_VERSION,
    unit="Unkown"
)

VOLTAGE = ObdData(
    name="Voltage",
    cmd=obd.commands.ELM_VOLTAGE,
    unit="Volts"
)

all_data = [
    # AUX_INPUT_STATUS,
    COOLANT_TEMP,
    ENGINE_LOAD,
    FUEL_STATUS,
    INTAKE_PRESSURE,
    INTAKE_TEMP,
    LONG_FUEL_TRIM_1,
    LONG_FUEL_TRIM_2,
    MAF,
    # MIDS_A,
    O2_B1S1,
    O2_B1S2,
    O2_B2S1,
    O2_B2S2,
    # O2_SENSORS,
    # OBD_COMPLIANCE,
    # PIDS_9A,
    # PIDS_A,
    RPM,
    SHORT_FUEL_TRIM_1,
    SHORT_FUEL_TRIM_2,
    SPEED,
    # STATUS,
    THROTTLE_POSITION,
    TIMING_ADVANCE,
    # VERSION,
    VOLTAGE,
]

# - DTC_INTAKE_TEMP
# - DTC_O2_B1S1
# - DTC_ENGINE_LOAD
# - DTC_O2_B2S1
# - DTC_RPM
# - DTC_O2_B1S2
# - DTC_SHORT_FUEL_TRIM_2
# - DTC_TIMING_ADVANCE
# - DTC_THROTTLE_POS
# - DTC_O2_SENSORS
# - DTC_OBD_COMPLIANCE
# - GET_CURRENT_DTC
# - DTC_INTAKE_PRESSURE
# - DTC_FUEL_STATUS
# - DTC_STATUS
# - DTC_LONG_FUEL_TRIM_1
# - DTC_O2_B2S2
# - DTC_MAF
# - CLEAR_DTC
# - DTC_AUX_INPUT_STATUS
# - DTC_SPEED
# - DTC_COOLANT_TEMP
# - DTC_LONG_FUEL_TRIM_2
# - GET_DTC
# - DTC_SHORT_FUEL_TRIM_1