#Meteor Shower (Multiple "meteors" falling randomly)
import time
import random
from pi5neo import Pi5Neo

def meteor_shower(neo, delay=0.1, meteor_length=3):
    while True:
        meteor_start = random.randint(0, neo.num_leds - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Meteor falling
        for i in range(meteor_start, meteor_start + meteor_length):
            neo.fill_strip(0, 0, 0)
            for j in range(meteor_length):
                if i - j >= 0 and i - j < neo.num_leds:
                    neo.set_led_color(i - j, *(int(color[k] * (1 - j / meteor_length)) for k in range(3)))
            neo.update_strip()
            time.sleep(delay)

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 8, 800)

# Random meteor shower effect
meteor_shower(neo)

