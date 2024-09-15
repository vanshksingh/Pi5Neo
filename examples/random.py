#Random LED Blink
import time
import random
from pi5neo import Pi5Neo

def random_blink(neo, num_blinks=10, delay=0.2):
    for _ in range(num_blinks):
        led_index = random.randint(0, neo.num_leds - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
        neo.set_led_color(led_index, *color)
        neo.update_strip()
        time.sleep(delay)
        neo.set_led_color(led_index, 0, 0, 0)  # Turn off the LED
        neo.update_strip()

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)
random_blink(neo)
