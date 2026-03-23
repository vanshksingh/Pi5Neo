# Theater chase: every third LED lights up and the pattern shifts
import time
from pi5neo import Pi5Neo


def theater_chase(neo, color, delay=0.1):
    """Classic theater-marquee chase effect, runs indefinitely."""
    while True:
        for offset in range(3):
            for i in range(neo.num_leds):
                if i % 3 == offset:
                    neo.set_led_color(i, *color)
                else:
                    neo.set_led_color(i, 0, 0, 0)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    theater_chase(neo, color=(0, 0, 255))
