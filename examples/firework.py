#Firework Animation (LEDs "explode" in different colors)
import time
import random
from pi5neo import Pi5Neo

def firework(neo, delay=0.05):
    center = random.randint(0, neo.num_leds - 1)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Simulate firework explosion expanding outward
    for radius in range(neo.num_leds):
        neo.fill_strip(0, 0, 0)
        if center - radius >= 0:
            neo.set_led_color(center - radius, *color)
        if center + radius < neo.num_leds:
            neo.set_led_color(center + radius, *color)
        neo.update_strip()
        time.sleep(delay)

# Initialize Pi5Neo with 10 LEDs
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Random fireworks effect
while True:
    firework(neo)

