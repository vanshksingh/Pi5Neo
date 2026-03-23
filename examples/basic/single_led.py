# Control a single LED on the strip
import time
from pi5neo import Pi5Neo


def control_single_led(neo, led_index, color, duration=2):
    """Set a specific LED to a color and hold for a duration."""
    neo.set_led_color(led_index, *color)
    neo.update_strip()
    time.sleep(duration)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    # Set the 3rd LED (index 2) to green
    control_single_led(neo, 2, (0, 255, 0))
