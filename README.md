# Pi5Neo

Pi5Neo is a Python library for controlling NeoPixel LED strips on Raspberry Pi 5 using SPI communication.

## Installation

pip install pi5neo
Usage

python
Copy code
from pi5neo import Pi5Neo

# Initialize the Pi5Neo class with 10 LEDs

pi5_neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Set the entire strip to red

pi5_neo.fill_strip(255, 0, 0)
pi5_neo.update_strip()
