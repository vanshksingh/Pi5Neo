# Thinking animation: strip cycles through colors to indicate "working"
import time
from pi5neo import Pi5Neo

COLORS = [
    (255, 255, 0),  # Yellow
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
]


def thinking_animation(neo, cycles=5, delay=0.1):
    """Flash the full strip through a set of colors for a given number of cycles."""
    for _ in range(cycles):
        for color in COLORS:
            neo.fill_strip(*color)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    thinking_animation(neo)
