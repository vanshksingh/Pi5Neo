#Controlling a Single LED
#This example shows how to control a single LED on a NeoPixel strip.
import time
from pi5neo import Pi5Neo

def control_single_led(neo, led_index, color, duration=2):
    neo.set_led_color(led_index, *color)  # Set a specific LED to the color
    neo.update_strip()  # Commit the change
    time.sleep(duration)  # Hold the color for a given duration

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Control the 3rd LED, set it to green
control_single_led(neo, 2, (0, 255, 0))
