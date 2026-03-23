# Firework: an explosion of color expands outward from a random center
import time
import random
from pi5neo import Pi5Neo


def firework(neo, delay=0.05):
    """Simulate one firework explosion expanding from a random position."""
    center = random.randint(0, neo.num_leds - 1)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    for radius in range(neo.num_leds):
        neo.fill_strip(0, 0, 0)
        left = center - radius
        right = center + radius
        if left >= 0:
            neo.set_led_color(left, *color)
        if right < neo.num_leds:
            neo.set_led_color(right, *color)
        neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    while True:
        firework(neo)
