# Loading bar: LEDs fill up one by one like a progress bar, then clear
import time
from pi5neo import Pi5Neo


def loading_bar(neo, color=(0, 255, 0), delay=0.1):
    """Fill LEDs from left to right, then clear, once."""
    for i in range(neo.num_leds):
        neo.set_led_color(i, *color)
        neo.update_strip(sleep_duration=delay)
    time.sleep(0.5)
    neo.clear_strip()
    neo.update_strip()


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    loading_bar(neo)
