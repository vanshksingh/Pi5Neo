# Color bounce: a single lit LED bounces back and forth
import time
from pi5neo import Pi5Neo


def color_bounce(neo, color, delay=0.05):
    """Bounce a single LED back and forth indefinitely."""
    while True:
        for i in range(neo.num_leds):
            neo.fill_strip(0, 0, 0)
            neo.set_led_color(i, *color)
            neo.update_strip(sleep_duration=delay)
        for i in range(neo.num_leds - 2, 0, -1):
            neo.fill_strip(0, 0, 0)
            neo.set_led_color(i, *color)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    color_bounce(neo, color=(0, 0, 255))
