import pygame

def draw_rpm_gauge(screen, rpm_value, font_small):
    """
    Draw RPM digital readout and shift bar.
    
    Args:
        screen: Pygame screen object
        rpm_value: Current RPM value
        font_large: Large font for RPM display
    """
    # Draw RPM number
    rpm_text = font_small.render(f"RPM: {rpm_value}", True, (255, 255, 255))
    screen.blit(rpm_text, (20, 20))
    
    bar_color = (0, 255, 0)

    if rpm_value <= 800:
        bar_color = (13, 255, 240)
    elif rpm_value > 800 and rpm_value <= 5000:
        bar_color = (0, 255, 0)
    else:
        bar_color = (255, 0, 0)

    # Draw RPM shift bar
    bar_width = min((rpm_value / 6000) * 400, 400)  # Cap at 400px
    # bar_color = (255, 0, 0) if rpm_value > 5000 else (0, 255, 0)
    pygame.draw.rect(screen, bar_color, (40, 70, bar_width, 40))


def draw_speed_gauge(screen, speed_value, font_small):
    """
    Draw speed display in MPH.
    
    Args:
        screen: Pygame screen object
        speed_value: Current speed in MPH
        font_small: Small font for speed display
    """
    speed_text = font_small.render(f"Speed: {speed_value} MPH", True, (255, 255, 0))
    screen.blit(speed_text, (20, 160))


def draw_coolant_gauge(screen, coolant_value, font_small):
    """
    Draw coolant temperature with color coding.
    Cyan when cold (<195°F), Orange when warm (>=195°F).
    
    Args:
        screen: Pygame screen object
        coolant_value: Current coolant temperature in Fahrenheit
        font_small: Small font for coolant display
    """
    coolant_color = (0, 255, 255) if coolant_value < 195 else (255, 100, 0)
    coolant_text = font_small.render(f"Coolant: {coolant_value}°F", True, coolant_color)
    screen.blit(coolant_text, (20, 200))


def draw_throttle_gauge(screen, throttle_value, font_small):
    """
    Draw throttle position percentage.
    
    Args:
        screen: Pygame screen object
        throttle_value: Current throttle position (0-100%)
        font_small: Small font for throttle display
    """
    throttle_text = font_small.render(f"Throttle: {throttle_value}%", True, (255, 255, 255))
    screen.blit(throttle_text, (20, 120))

    bar_width = min((throttle_value / 100) * 780, 780)  # Cap at 400px
    bar_color = (255, 0, 0) if throttle_value > 50 else (0, 255, 0)
    pygame.draw.rect(screen, bar_color, (40, 170, bar_width, 40))

def draw_load_gauge(screen, load_value, font_small):
    load_text = font_small.render(f"Engine Load: {load_value}%", True, (255, 255, 255))
    screen.blit(load_text, (20, 220))

    bar_width = min((load_value / 100) * 780, 780)  # Cap at 400px
    bar_color = (255, 0, 0) if load_value > 50 else (0, 255, 0)
    pygame.draw.rect(screen, bar_color, (40, 270, bar_width, 40))

def draw_voltage_gauge(screen, voltage_value, font_small):
    voltage_text = font_small.render(f"Voltage: {voltage_value}V", True, (255, 255, 0))
    screen.blit(voltage_text, (20, 280))


def draw_gear_gauge(screen, gear_value, font_small):
    """
    Draw estimated gear display.
    
    Args:
        screen: Pygame screen object
        gear_value: Estimated gear string (e.g., "3rd", "4th (OD)")
        font_large: Large font for gear display
    """
    # Color coding: Green for normal driving gears, Yellow for 1st/overdrive
    if gear_value in ["2nd", "3rd"]:
        gear_color = (0, 255, 0)  # Green
    elif gear_value == "1st":
        gear_color = (255, 255, 0)  # Yellow
    elif gear_value == "4th (OD)":
        gear_color = (0, 200, 255)  # Light blue for overdrive
    else:
        gear_color = (150, 150, 150)  # Gray for N/P or unknown
    
    gear_text = font_small.render(f"Gear: {gear_value}", True, gear_color)
    screen.blit(gear_text, (20, 320))


def render_display(screen, data_store, font_large, font_small):
    """
    Main rendering function - draws all gauges on screen.
    
    Args:
        screen: Pygame screen object
        data_store: Dictionary containing all sensor data
        font_large: Large font object
        font_small: Small font object
    """
    # Clear screen
    screen.fill((0, 0, 0))  # Black background
    
    # Get values from data store
    rpm_value = data_store.get('RPM', 0)
    speed_value = data_store.get('Speed', 0)
    coolant_value = data_store.get('Coolant Temperature', 0)
    throttle_value = data_store.get('Throttle Position', 0)
    voltage_value = data_store.get('Voltage', 0)
    gear_value = data_store.get('Estimated Gear', '---')
    load_value = data_store.get('Engine Load', 0)
    
    # Draw all gauges
    draw_rpm_gauge(screen, rpm_value, font_small)
    # draw_speed_gauge(screen, speed_value, font_small)
    # draw_coolant_gauge(screen, coolant_value, font_small)
    draw_throttle_gauge(screen, throttle_value, font_small)
    # draw_voltage_gauge(screen, voltage_value, font_small)
    draw_gear_gauge(screen, gear_value, font_small)
    draw_load_gauge(screen, load_value, font_small)
    
    # Update display
    pygame.display.flip()