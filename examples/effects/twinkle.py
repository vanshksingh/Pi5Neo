# Twinkle: random LEDs flash on and off like stars
import time
import random
from pi5neo import Pi5Neo


def twinkle(neo, num_twinkles=5, delay=0.1):
    """Flash random LEDs in random bright colors."""
    for _ in range(num_twinkles):
        led_index = random.randint(0, neo.num_leds - 1)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        neo.set_led_color(led_index, *color)
        neo.update_strip(sleep_duration=delay)
        neo.set_led_color(led_index, 0, 0, 0)
        neo.update_strip(sleep_duration=None)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    while True:
        twinkle(neo)
