import time
import subprocess
from gpiozero import Button
from yukon_watcher.constants.pi_pins import PiPins

class HardwareManager:
    def __init__(self):
        # 1. Listeners / Inputs
        self.auto_start_button = Button(PiPins.AUTO_START.value, pull_up=True)
        self.off_button = Button(PiPins.POWER_OFF.value, pull_up=True)

        # Attach the power-off callback automatically on press
        self.off_button.when_pressed = self._power_off_callback

    def is_auto_start_pressed(self) -> bool:
        return self.auto_start_button.is_pressed

    def _power_off_callback(self) -> None:
        """Runs in the background when the POWER_OFF button is pressed."""
        # would be cool if this played the animation on the display in reverse
        print("\n==================================================")
        print(" SHUTDOWN BUTTON PRESSED! ")
        print(" Stopping telemetry and powering down in 3s...")
        print(" Goodbye ")
        print("==================================================\n")

        time.sleep(3)

        # Stop systemd service first so it won't auto-restart
        subprocess.run(["sudo", "systemctl", "stop", "yukon.service"])

        # Execute system shutdown command
        subprocess.run(["sudo", "/sbin/poweroff"])