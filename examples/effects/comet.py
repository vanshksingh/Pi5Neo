# Comet trail: a moving LED with a fading tail
import time
from pi5neo import Pi5Neo


def comet_trail(neo, color, trail_length=5, delay=0.1):
    """Animate a comet with a fading trail indefinitely."""
    while True:
        for i in range(neo.num_leds + trail_length):
            neo.fill_strip(0, 0, 0)
            for j in range(trail_length):
                pos = i - j
                if 0 <= pos < neo.num_leds:
                    intensity = int(255 * (1 - j / trail_length))
                    scaled = tuple(intensity if ch > 0 else 0 for ch in color)
                    neo.set_led_color(pos, *scaled)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    comet_trail(neo, color=(0, 0, 255))
