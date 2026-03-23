# Smooth cosine fade: per-LED brightness varies using a cosine wave over time
from math import cos
import time
from pi5neo import Pi5Neo


def smooth_fade(neo):
    """Apply a time-varying cosine brightness wave across all LEDs."""
    t = time.time()
    for i in range(neo.num_leds):
        intensity = int((cos(i * 0.01 + t) * 0.5 + 0.5) * 255)
        neo.set_led_color(i, intensity, intensity, intensity)
    neo.update_strip(sleep_duration=0.01)


with Pi5Neo('/dev/spidev0.0', num_leds=300, spi_speed_khz=800, quiet_mode=True) as neo:
    while True:
        smooth_fade(neo)
