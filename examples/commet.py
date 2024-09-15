#Comet Trail (A moving LED with a trailing fade effect)
import time
from pi5neo import Pi5Neo

def comet_trail(neo, color, delay=0.1):
    num_leds = neo.num_leds
    trail_length = 5  # Length of the comet trail
    
    while True:
        for i in range(num_leds + trail_length):
            neo.fill_strip(0, 0, 0)  # Clear the strip
            for j in range(trail_length):
                if 0 <= i - j < num_leds:
                    # Set the color of the comet trail (fading)
                    intensity = int(255 * (1 - (j / trail_length)))
                    neo.set_led_color(i - j, *(intensity if c > 0 else 0 for c in color))
            neo.update_strip()
            time.sleep(delay)

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Blue comet trail effect
comet_trail(neo, (0, 0, 255))
