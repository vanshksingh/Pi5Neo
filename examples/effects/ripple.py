# Ripple: color waves expand outward from the center of the strip
import time
from pi5neo import Pi5Neo


def ripple(neo, color, delay=0.1):
    """Expand a ripple outward from the center indefinitely."""
    center = neo.num_leds // 2
    while True:
        for radius in range(neo.num_leds // 2 + 1):
            neo.fill_strip(0, 0, 0)
            left = center - radius
            right = center + radius
            if left >= 0:
                neo.set_led_color(left, *color)
            if right < neo.num_leds:
                neo.set_led_color(right, *color)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    ripple(neo, color=(0, 0, 255))
