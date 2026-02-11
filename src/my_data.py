from args import parser

args = parser.parse_args()

if args.testing == True:
    import fake_obd as obd
    connection = obd.FakeOBD()

else:
    import obd
    connection = obd.OBD(portstr="/dev/ttyUSB0")

class Conversion:
    def __init__(self, amount, offset = 0):
        self.amount = amount
        self.offset = offset

class ObdData:
    def __init__(self, name, cmd, unit, textToReplace = None, conversion = None,):
        self.name = name
        self.cmd = cmd
        self.unit = unit
        self.textToReplace = textToReplace
        self.conversion = conversion
    
    @property 
    def response(self):
        myresponse = connection.query(self.cmd)
        if self.textToReplace is not None:
            stringResponse = str(myresponse)
            cleanedResponse = stringResponse.replace(self.textToReplace, "")
            unConvertedResponse = float(cleanedResponse)
            if self.conversion is not None:
                convertedResponse = unConvertedResponse * self.conversion.amount + self.conversion.offset
                return round(convertedResponse)
            else:
                return round(unConvertedResponse)
        else: 
            return myresponse

AUX_INPUT_STATUS = ObdData(
    name="Auxillary Input",
    cmd=obd.commands.AUX_INPUT_STATUS,
    unit="Unkown",
)

COOLANT_TEMP = ObdData(
    name="Coolant Tempurature",
    cmd=obd.commands.COOLANT_TEMP,
    unit="Fahrenheit",
    textToReplace=" degree_Celsius",
    conversion = Conversion(amount= 1.8, offset= 32) 
    )

ENGINE_LOAD = ObdData(
    name="Engine Load",
    cmd=obd.commands.ENGINE_LOAD,
    unit="Percentage",
    textToReplace=" percent"
)

FUEL_STATUS = ObdData(
    name="Fuel Status",
    cmd=obd.commands.FUEL_STATUS,
    unit="Open Loop, Open Loop or Closed Loop, Closed Loop based on temp",
)

INTAKE_PRESSURE = ObdData(
    name="Intake Pressure",
    cmd=obd.commands.INTAKE_PRESSURE,
    unit="kilopascal",
    textToReplace=" kilopascal"
)

INTAKE_TEMP = ObdData(
    name="Intake Tempurature",
    cmd=obd.commands.INTAKE_TEMP,
    unit="Celsius",
    textToReplace=" degree_celsius"
)

LONG_FUEL_TRIM_1 = ObdData(
    name="Bank 1 Long Fuel Trim",
    cmd=obd.commands.LONG_FUEL_TRIM_1,
    unit="Percentage",
    textToReplace=" percent"
)

LONG_FUEL_TRIM_2 = ObdData(
    name="Bank 2 Long Fuel Trim",
    cmd=obd.commands.LONG_FUEL_TRIM_2,
    unit="Percentage",
    textToReplace=" percent"
)

MAF = ObdData(
    name="Mass Airflow Sensor",
    cmd=obd.commands.MAF,
    unit="Grams Per Second",
    textToReplace=" gps"
)

MIDS_A = ObdData(
    name="MIDS A",
    cmd=obd.commands.MIDS_A,
    unit="None",
)

O2_B1S1 = ObdData(
    name="O2 Bank 1 Sensor 1",
    cmd=obd.commands.O2_B1S1,
    unit="Volts",
    textToReplace=" volt"
)

O2_B1S2 = ObdData(
    name="O2 Bank 1 Sensor 2",
    cmd=obd.commands.O2_B1S2,
    unit="Volts",
    textToReplace=" volt"
)

O2_B2S1 = ObdData(
    name="O2 Bank 2 Sensor 1",
    cmd=obd.commands.O2_B2S1,
    unit="Volts",
    textToReplace=" volt"
)

O2_B2S2 = ObdData(
    name="O2 Bank 2 Sensor 2",
    cmd=obd.commands.O2_B2S2,
    unit="Volts",
    textToReplace=" volt"
)

O2_SENSORS = ObdData(
    name="O2 Sensors Status",
    cmd=obd.commands.O2_SENSORS,
    unit="(false, false, true, true) (false, false, true, true)",
)

OBD_COMPLIANCE = ObdData(
    name="OBD Compliance",
    cmd=obd.commands.OBD_COMPLIANCE,
    unit="String",
)

PIDS_9A = ObdData(
    name="PIDS 9A",
    cmd=obd.commands.PIDS_9A,
    unit="Bitmask",
)

PIDS_A = ObdData(
    name="PIDS A",
    cmd=obd.commands.PIDS_A,
    unit="Bitmask", 
)

RPM = ObdData(
    name="RPM",
    cmd=obd.commands.RPM,
    unit="Revolutions Per Minute",
    textToReplace=" revolutions_per_minute"
)

SHORT_FUEL_TRIM_1 = ObdData(
    name="Bank 1 Short Fuel Trim",
    cmd=obd.commands.SHORT_FUEL_TRIM_1,
    unit="Percent",
    textToReplace=" percent"
)

SHORT_FUEL_TRIM_2 = ObdData(
    name="Bank 2 Short Fuel Trim",
    cmd=obd.commands.SHORT_FUEL_TRIM_2,
    unit="Percent",
    textToReplace=" percent"
)

SPEED = ObdData(
    name="Speed",
    cmd=obd.commands.SPEED,
    unit="MPH",
    textToReplace=" kilometer_per_hour",
    conversion= Conversion(amount= 0.621371)
)

STATUS = ObdData(
    name="OBD Status",
    cmd=obd.commands.STATUS,
    unit="Unkown",
)

THROTTLE_POSITION = ObdData(
    name="Throttle Position",
    cmd=obd.commands.THROTTLE_POS,
    unit="Percent",
    textToReplace=" percent"
)

TIMING_ADVANCE = ObdData(
    name="Timing Advance",
    cmd=obd.commands.TIMING_ADVANCE,
    unit="Degrees",
    textToReplace=" degree"
)
# maybe display this on startup
VERSION = ObdData(
    name="Firmware Version",
    cmd=obd.commands.ELM_VERSION,
    unit="String", 
)

VOLTAGE = ObdData(
    name="Voltage",
    cmd=obd.commands.ELM_VOLTAGE,
    unit="Volts",
    textToReplace=" volt"
)

all_data = [
    # AUX_INPUT_STATUS,
    # COOLANT_TEMP,
    # ENGINE_LOAD,
    # FUEL_STATUS,
    # INTAKE_PRESSURE,
    # INTAKE_TEMP,
    # LONG_FUEL_TRIM_1,
    # LONG_FUEL_TRIM_2,
    # MAF,
    # MIDS_A,
    # O2_B1S1,
    # O2_B1S2,
    # O2_B2S1,
    # O2_B2S2,
    # O2_SENSORS,
    # OBD_COMPLIANCE,
    # PIDS_9A,
    # PIDS_A,
    RPM,
    # SHORT_FUEL_TRIM_1,
    # SHORT_FUEL_TRIM_2,
    SPEED,
    # STATUS,
    # THROTTLE_POSITION,
    # TIMING_ADVANCE,
    # VERSION,
    # VOLTAGE,
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