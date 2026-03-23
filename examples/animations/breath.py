# Breathing effect: a single LED slowly fades in and out
import time
from pi5neo import Pi5Neo


def breathing_led(neo, led_index, color, steps=50, delay=0.05):
    """Pulse one LED in and out indefinitely."""
    while True:
        for i in range(steps):
            intensity = int(255 * i / steps)
            scaled = tuple(intensity if ch > 0 else 0 for ch in color)
            neo.set_led_color(led_index, *scaled)
            neo.update_strip(sleep_duration=delay)
        for i in range(steps, 0, -1):
            intensity = int(255 * i / steps)
            scaled = tuple(intensity if ch > 0 else 0 for ch in color)
            neo.set_led_color(led_index, *scaled)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    breathing_led(neo, led_index=0, color=(255, 0, 0))
