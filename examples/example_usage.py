#basic example of using the Pi5Neo class to control a NeoPixel strip
from pi5neo import Pi5Neo  # Import the Pi5Neo class
import time

def demo_solid_color(neo, red, green, blue, duration=2):
    """Set the entire strip to a solid color and hold for a duration"""
    neo.fill_strip(red, green, blue)
    neo.update_strip()
    time.sleep(duration)

def demo_rainbow_cycle(neo, delay=0.1):
    """Cycle through rainbow colors on the entire strip"""
    rainbow_colors = [
        (255, 0, 0),  # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211)  # Violet
    ]
    for color in rainbow_colors:
        neo.fill_strip(*color)
        neo.update_strip()
        time.sleep(delay)

# Initialize the Pi5Neo class with 10 LEDs
pi5_neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Run demo functions
demo_solid_color(pi5_neo, 255, 0, 0)  # Red strip
demo_rainbow_cycle(pi5_neo)  # Rainbow cycle effect
