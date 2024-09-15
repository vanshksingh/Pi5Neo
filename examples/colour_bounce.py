# Color Bounce Animation (LED color "bounces" back and forth)
import time
from pi5neo import Pi5Neo

def color_bounce(neo, color, delay=0.05):
    num_leds = neo.num_leds
    while True:
        # Forward bounce
        for i in range(num_leds):
            neo.fill_strip(0, 0, 0)  # Clear the strip
            neo.set_led_color(i, *color)  # Set the current LED to the color
            neo.update_strip()
            time.sleep(delay)
        
        # Backward bounce
        for i in range(num_leds - 1, -1, -1):
            neo.fill_strip(0, 0, 0)  # Clear the strip
            neo.set_led_color(i, *color)  # Set the current LED to the color
            neo.update_strip()
            time.sleep(delay)

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Bouncing blue light
color_bounce(neo, (0, 0, 255))
