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

coolant_temp = ObdData(
    name="Coolant Tempurature",
    cmd=obd.commands.COOLANT_TEMP,
    unit="Celsius"
)

elm_voltage = ObdData(
    name="Voltage",
    cmd=obd.commands.ELM_VOLTAGE,
    unit="Volts"
)

speed = ObdData(
    name="Speed",
    cmd=obd.commands.SPEED,
    unit="Kilometers"
)

rpm = ObdData(
    name="RPM",
    cmd=obd.commands.RPM,
    unit="RPM"
)

throttle_pos = ObdData(
    name="Throttle Position",
    cmd=obd.commands.THROTTLE_POS,
    unit="Unkown"
)

intake_temp = ObdData(
    name="Intake Tempurature",
    cmd=obd.commands.INTAKE_TEMP,
    unit="Celsius"
)

engine_load = ObdData(
    name="Engine Load",
    cmd=obd.commands.ENGINE_LOAD,
    unit=" Percentage"
)

aux_input = ObdData(
    name="Auxillary Input",
    cmd=obd.commands.AUX_INPUT_STATUS,
    unit="Unkown"
)

o2_b1s1 = ObdData(
    name="O2 Bank 1 Sensor 1",
    cmd=obd.commands.O2_B1S1,
    unit="Volts"
)

o2_b1s2 = ObdData(
    name="O2 Bank 1 Sensor 2",
    cmd=obd.commands.O2_B1S2,
    unit="Volts"
)

o2_b2s1 = ObdData(
    name="O2 Bank 2 Sensor 1",
    cmd=obd.commands.O2_B2S1,
    unit="Volts"
)

o2_b2s2 = ObdData(
    name="O2 Bank 2 Sensor 2",
    cmd=obd.commands.O2_B2S2,
    unit="Volts"
)

o2_sensors = ObdData(
    name="O2 Sensors Status",
    cmd=obd.commands.O2_SENSORS,
    unit="Unkown"
)

timing = ObdData(
    name="Timing Advance",
    cmd=obd.commands.TIMING_ADVANCE,
    unit="Degrees"
)

# maybe display this on startup
version = ObdData(
    name="Firmware Version",
    cmd=obd.commands.ELM_VERSION,
    unit="Unkown"
)

maf = ObdData(
    name="Mass Airflow Sensor",
    cmd=obd.commands.MAF,
    unit="Unkown"
)

intake_pressure = ObdData(
    name="Intake Pressure",
    cmd=obd.commands.INTAKE_PRESSURE,
    unit="kilopascal"
)

b1_short_fuel_trim = ObdData(
    name="Bank 1 Short Fuel Trim",
    cmd=obd.commands.SHORT_FUEL_TRIM_1,
    unit="Unkown"
)

b2_short_fuel_trim = ObdData(
    name="Bank 2 Short Fuel Trim",
    cmd=obd.commands.SHORT_FUEL_TRIM_2,
    unit="Unkown"
)

b1_long_fuel_trim = ObdData(
    name="Bank 1 Long Fuel Trim",
    cmd=obd.commands.LONG_FUEL_TRIM_1,
    unit="Percentage"
)

b2_long_fuel_trim = ObdData(
    name="Bank 2 Long Fuel Trim",
    cmd=obd.commands.LONG_FUEL_TRIM_2,
    unit="Percentage"
)

fuel_status = ObdData(
    name="Fuel Status",
    cmd=obd.commands.FUEL_STATUS,
    unit="Unkown"
)

obd_status = ObdData(
    name="OBD Status",
    cmd=obd.commands.STATUS,
    unit="Unkown"
)

pids_a = ObdData(
    name="PIDS A",
    cmd=obd.commands.PIDS_A,
    unit="Unkown"
)

pids_9a = ObdData(
    name="PIDS 9A",
    cmd=obd.commands.PIDS_9A,
    unit="Unkown"
)

obd_compliance = ObdData(
    name="OBD Compliance",
    cmd=obd.commands.OBD_COMPLIANCE,
    unit="Unkown"
)

mids_a = ObdData(
    name="MIDS A",
    cmd=obd.commands.MIDS_A,
    unit="Unkown"
)

all_data = [
    # o2_sensors,
    # version,
    maf,
    b1_short_fuel_trim,
    b2_short_fuel_trim,
    fuel_status,
    # obd_status,
    # pids_a,
    # pids_9a,
    # obd_compliance,
    # mids_a,
    coolant_temp,
    intake_temp,
    b1_long_fuel_trim,
    b2_long_fuel_trim,
    intake_pressure,
    timing,
    engine_load,
    o2_b1s1,
    o2_b1s2,
    o2_b2s1,
    o2_b2s2,
    elm_voltage,
    speed,
    rpm,
    throttle_pos,
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