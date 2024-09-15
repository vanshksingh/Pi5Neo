#Loading Bar Effect with Single LED Moving
import time
from pi5neo import Pi5Neo

def loading_bar(neo, delay=0.1):
    for i in range(neo.num_leds):
        neo.fill_strip(0, 0, 0)  # Clear the strip
        neo.set_led_color(i, 0, 255, 0)  # Set a green color for the current LED
        neo.update_strip()
        time.sleep(delay)

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)
loading_bar(neo)
