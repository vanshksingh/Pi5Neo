# Meteor shower: random meteors fall with a fading trail
import time
import random
from pi5neo import Pi5Neo


def meteor_shower(neo, meteor_length=3, delay=0.1):
    """Spawn random meteors with fading trails, runs indefinitely."""
    while True:
        start = random.randint(0, neo.num_leds - 1)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        for i in range(start, start + meteor_length):
            neo.fill_strip(0, 0, 0)
            for j in range(meteor_length):
                pos = i - j
                if 0 <= pos < neo.num_leds:
                    fade = 1 - j / meteor_length
                    scaled = tuple(int(ch * fade) for ch in color)
                    neo.set_led_color(pos, *scaled)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    meteor_shower(neo)
