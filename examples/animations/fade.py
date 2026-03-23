# Color fade: every LED smoothly transitions through a list of colors
import time
from pi5neo import Pi5Neo


def color_fade(neo, colors, steps=100, delay=0.02):
    """Smoothly fade the entire strip through the given color list."""
    num_colors = len(colors)
    while True:
        for i in range(num_colors):
            start = colors[i]
            end = colors[(i + 1) % num_colors]
            for step in range(steps):
                blended = tuple(
                    int(start[c] + (end[c] - start[c]) * step / steps)
                    for c in range(3)
                )
                neo.fill_strip(*blended)
                neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    color_fade(neo, [(255, 0, 0), (0, 255, 0), (0, 0, 255)])
