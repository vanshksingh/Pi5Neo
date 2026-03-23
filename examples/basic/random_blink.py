# Random LED blink: lights a random LED in a random color, then turns it off
import time
import random
from pi5neo import Pi5Neo


def random_blink(neo, num_blinks=10, delay=0.2):
    """Blink random LEDs in random colors."""
    for _ in range(num_blinks):
        led_index = random.randint(0, neo.num_leds - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        neo.set_led_color(led_index, *color)
        neo.update_strip()
        time.sleep(delay)
        neo.set_led_color(led_index, 0, 0, 0)
        neo.update_strip()


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    random_blink(neo)
