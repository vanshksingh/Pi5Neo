# Demonstrates LEDColor dataclass: set_led_color_object() and get_led_color()
import time
from pi5neo import Pi5Neo, LEDColor


def shift_colors(neo):
    """Read each LED's current color, shift it one position forward, then write back."""
    last = neo.get_led_color(neo.num_leds - 1)
    for i in range(neo.num_leds - 1, 0, -1):
        prev = neo.get_led_color(i - 1)
        neo.set_led_color_object(i, prev)
    neo.set_led_color_object(0, last)


# Seed the strip with distinct colors using LEDColor objects
seed_colors = [
    LEDColor(red=255, green=0,   blue=0),    # red
    LEDColor(red=0,   green=255, blue=0),    # green
    LEDColor(red=0,   green=0,   blue=255),  # blue
    LEDColor(red=255, green=255, blue=0),    # yellow
    LEDColor(red=0,   green=255, blue=255),  # cyan
]

with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    for i, color in enumerate(seed_colors):
        neo.set_led_color_object(i, color)
    neo.update_strip()
    time.sleep(1)

    # Rotate colors along the strip 20 times
    for _ in range(20):
        shift_colors(neo)
        neo.update_strip(sleep_duration=0.1)
