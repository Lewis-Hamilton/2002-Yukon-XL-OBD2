import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

# Global or module-level I2C initialization
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48)

# Select gain for +/- 4.096V range (1 bit = 0.125mV)
ads.gain = 1


def get_hsts016l_current_amps(
    ads_instance: ADS.ADS1115 = ads, mv_per_amp: float = 62.5
) -> float | None:
    """
    Reads differential voltage between A0 (Vout) and A1 (Vref) on ADS1115
    and converts to current in Amperes.
    Returns None if I2C or hardware reading fails.
    """
    try:
        # Measure differential input A0 - A1
        chan = AnalogIn(ads_instance, ADS.P0, ADS.P1)

        # chan.voltage returns value in Volts; convert to millivolts
        diff_voltage_mv = chan.voltage * 1000.0

        # Convert mV delta to Amperes
        current_amps = diff_voltage_mv / mv_per_amp

        return round(current_amps, 3)
    except (OSError, ValueError, AttributeError):
        return None
