import os
import signal
import subprocess
import time

from gpiozero import Button

from yukon_watcher.constants.pi_pins import PiPins

SHUTDOWN_GRACE = 2  # Give the graceful exit time to actually finish


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

        # 1. Spawn poweroff in a detached background subprocess so it executes
        # regardless of this Python process being terminated.
        subprocess.Popen(["sudo", "/sbin/poweroff"])

        # 2. Stop systemd service to prevent auto-restart race conditions
        subprocess.run(["sudo", "systemctl", "stop", "yukon.service"], check=False)

        # 3. Now signal SIGTERM so main.py runs its graceful cleanup/CSV flush
        os.kill(os.getpid(), signal.SIGTERM)
