import RPi.GPIO as GPIO

def monitor_shutdown_button():
    while True:
        # Check if button is pressed (LOW)
        # would be cool if this played the animation on the display in reverse
        if GPIO.input(SHUTDOWN_PIN) == GPIO.LOW:
            print("\n==================================================")
            print(" SHUTDOWN BUTTON PRESSED! ")
            print(" Stopping telemetry and powering down in 3s...")
            print("==================================================\n")
            
            # Allow clean up of serial/logging if needed
            time.sleep(3)
            
            # Execute system shutdown command
            subprocess.run(["sudo", "/sbin/poweroff"])
            break
            
        time.sleep(0.2)