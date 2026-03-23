# Snake effect: a short block of lit LEDs slides across the strip
import time
from pi5neo import Pi5Neo


def snake_effect(neo, color, snake_length=3, delay=0.05):
    """Slide a block of LEDs across the strip indefinitely."""
    while True:
        for i in range(neo.num_leds + snake_length):
            neo.fill_strip(0, 0, 0)
            for j in range(snake_length):
                pos = i - j
                if 0 <= pos < neo.num_leds:
                    neo.set_led_color(pos, *color)
            neo.update_strip(sleep_duration=delay)


with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    snake_effect(neo, color=(0, 255, 0))
