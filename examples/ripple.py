#Ripple Effect (Color waves ripple outwards from a center point)
import time
from pi5neo import Pi5Neo

def ripple(neo, color, delay=0.1):
    center = neo.num_leds // 2  # Center of the strip
    while True:
        for radius in range(neo.num_leds // 2 + 1):
            neo.fill_strip(0, 0, 0)
            if center - radius >= 0:
                neo.set_led_color(center - radius, *color)
            if center + radius < neo.num_leds:
                neo.set_led_color(center + radius, *color)
            neo.update_strip()
            time.sleep(delay)

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Blue ripple effect from center
ripple(neo, (0, 0, 255))
