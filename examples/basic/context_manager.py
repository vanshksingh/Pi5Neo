# Demonstrates the context manager: strip is always cleared and SPI closed on exit,
# even if an exception is raised mid-animation.
import time
from pi5neo import Pi5Neo


def flash_red(neo, times=5, delay=0.3):
    """Flash the entire strip red."""
    for _ in range(times):
        neo.fill_strip(255, 0, 0)
        neo.update_strip(sleep_duration=None)  # skip built-in delay
        time.sleep(delay)
        neo.clear_strip()
        neo.update_strip(sleep_duration=None)
        time.sleep(delay)


# The 'with' block guarantees clear_strip() + spi.close() are called on exit.
with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    flash_red(neo)
    # Strip is automatically cleared and SPI released here
