#Twinkle Effect (Random LEDs twinkle on and off)
import time
import random
from pi5neo import Pi5Neo

def twinkle(neo, num_twinkles=5, delay=0.1):
    for _ in range(num_twinkles):
        led_index = random.randint(0, neo.num_leds - 1)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        neo.set_led_color(led_index, *color)
        neo.update_strip()
        time.sleep(delay)
        neo.set_led_color(led_index, 0, 0, 0)  # Turn off the LED
        neo.update_strip()

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Continuous twinkle effect
while True:
    twinkle(neo)