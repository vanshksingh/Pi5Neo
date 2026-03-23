# Demonstrates EPixelType: choose the correct channel order for your LED strip
# WS2812B strips are usually GRB; SK6812 RGBW strips add a white channel.
import time
from pi5neo import Pi5Neo, EPixelType


def show_colors(neo, duration=1.0):
    """Cycle red → green → blue → white (if RGBW) to verify channel order."""
    colors = [
        (255, 0, 0, 0),   # Red
        (0, 255, 0, 0),   # Green
        (0, 0, 255, 0),   # Blue
    ]
    if neo.pixel_type in (EPixelType.RGBW, EPixelType.GRBW):
        colors.append((0, 0, 0, 255))  # White channel only

    for r, g, b, w in colors:
        neo.fill_strip(r, g, b, w)
        neo.update_strip()
        time.sleep(duration)


# --- GRB strip (most common WS2812B) ---
print("Testing GRB strip")
with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800,
            pixel_type=EPixelType.GRB, quiet_mode=True) as neo:
    show_colors(neo)

# --- RGBW strip (SK6812 with dedicated white channel) ---
print("Testing RGBW strip")
with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800,
            pixel_type=EPixelType.RGBW, quiet_mode=True) as neo:
    show_colors(neo)
