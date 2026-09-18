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
    ads_instance: ADS.ADS1115 = ads,
    mv_per_amp: float = 3.125,
    zero_offset_mv: float = 7.0,  # Baseline offset with 0 Amps passing through sensor
    deadband_amps: float = 0.5,
) -> float | None:
    """
    Reads differential voltage between A0 (Vout) and A1 (Vref) on ADS1115
    and converts to current in Amperes, accounting for baseline offset.
    """
    try:
        # Measure differential input A0 - A1
        chan_diff = AnalogIn(ads_instance, 0, 1)
        raw_diff_mv = chan_diff.voltage * 1000.0

        # Subtract baseline hardware offset (7.0 mV)
        calibrated_diff_mv = raw_diff_mv - zero_offset_mv

        # Convert calibrated mV delta to Amperes
        current_amps = calibrated_diff_mv / mv_per_amp

        # Filter out minor idle noise around zero
        if abs(current_amps) < deadband_amps:
            current_amps = 0.0

        return round(current_amps, 2)
    except (OSError, ValueError, AttributeError) as e:
        print(f"[DEBUG] Error reading ADS1115: {e}")
        return None
