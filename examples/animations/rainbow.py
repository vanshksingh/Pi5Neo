# Rainbow wave: rainbow colors scroll continuously across the strip
import time
from pi5neo import Pi5Neo

COLORS = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211),  # Violet
]


def running_rainbow(neo, delay=0.05):
    """Scroll rainbow colors across the strip indefinitely."""
    num_colors = len(COLORS)
    while True:
        for offset in range(neo.num_leds):
            for i in range(neo.num_leds):
                neo.set_led_color(i, *COLORS[(i + offset) % num_colors])
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    running_rainbow(neo)
