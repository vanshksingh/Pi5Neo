# Pi5Neo

### Simplifying NeoPixel LED Control on Raspberry Pi 5 via SPI

[![PyPI version](https://badge.fury.io/py/Pi5Neo.svg)](https://badge.fury.io/py/Pi5Neo) 
[![Python Versions](https://img.shields.io/pypi/pyversions/Pi5Neo.svg)](https://pypi.org/project/Pi5Neo)
[![License](https://img.shields.io/github/license/vanshksingh/Pi5Neo)](LICENSE)

![IMG_7596](https://github.com/user-attachments/assets/6fb727ae-789e-4d25-9dd7-38599fdbb81e)

Pi5Neo is a Python library designed to make controlling **NeoPixel LED strips** super easy and efficient on the **Raspberry Pi 5** (or equivalent boards). Whether you're creating dazzling light shows, informative displays, or ambient lighting, Pi5Neo simplifies the process using the Raspberry Pi’s **SPI interface** for high-performance communication.

## 🌟 Key Features

- **Easy NeoPixel Control**: Send commands to any NeoPixel LED strip connected to the Raspberry Pi 5’s SPI interface.
- **Smooth Transitions**: Enjoy vibrant color transitions with rainbow effects, loading bars, blinking patterns, and more.
- **Optimized for Performance**: Tailored for the Raspberry Pi 5, ensuring fast and reliable communication with NeoPixel strips.
- **Minimalistic API**: A simple API lets you focus on creativity without worrying about low-level hardware details.
- **Flexible Configurations**: Control various effects and animations by easily setting colors, durations, and brightness levels.

## 🚀 Installation

You can install Pi5Neo via `pip`:

```bash
pip install pi5neo
```

### Requirements
- **Python 3.6+**
- **spidev** (automatically installed with Pi5Neo)

### Hardware
- **Raspberry Pi 5** (or equivalent with SPI interface)
- **NeoPixel LED Strip** (WS281x family)

## 📚 Usage

Pi5Neo makes it straightforward to set up and control your NeoPixel strip. Here's a simple example:

```python
from pi5neo import Pi5Neo

# Initialize the Pi5Neo class with 10 LEDs and an SPI speed of 800kHz
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Fill the strip with a red color
neo.fill_strip(255, 0, 0)
neo.update_strip()  # Commit changes to the LEDs

# Set the 5th LED to blue
neo.set_led_color(4, 0, 0, 255)
neo.update_strip()
```

## 🌈 Examples

You can find more advanced examples in the [examples](examples) directory. Here’s a quick showcase of some cool effects you can create with Pi5Neo:

### Example 1: Rainbow Cycle
```python
from pi5neo import Pi5Neo
import time

def rainbow_cycle(neo, delay=0.1):
    colors = [
        (255, 0, 0),  # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211)  # Violet
    ]
    for color in colors:
        neo.fill_strip(*color)
        neo.update_strip()
        time.sleep(delay)

neo = Pi5Neo('/dev/spidev0.0', 10, 800)
rainbow_cycle(neo)
```

### Example 2: Loading Bar Effect
```python
from pi5neo import Pi5Neo
import time

def loading_bar(neo):
    for i in range(neo.num_leds):
        neo.set_led_color(i, 0, 255, 0)  # Green loading bar
        neo.update_strip()
        time.sleep(0.2)
    neo.clear_strip()
    neo.update_strip()

neo = Pi5Neo('/dev/spidev0.0', 10, 800)
loading_bar(neo)
```


## ⚙️ Configuration

You can configure Pi5Neo by passing in different parameters for the number of LEDs, SPI speed, and more:

```python
Pi5Neo('/dev/spidev0.0', num_leds=20, spi_speed_khz=1000)
```

- **`/dev/spidev0.0`**: SPI device path
- **`num_leds`**: Number of LEDs in the NeoPixel strip
- **`spi_speed_khz`**: SPI speed in kHz (default 800)

## 🛠️ Contributing

We welcome contributions from the community! To contribute:

1. Fork the repo.
2. Create a new branch (`git checkout -b my-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin my-feature`).
5. Create a new Pull Request.

Feel free to open issues for bugs, questions, or feature requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❤️ Acknowledgements

Pi5Neo was inspired by various open-source projects that aim to make hardware control easier and more accessible. Special thanks to the contributors of `spidev` and Raspberry Pi for their amazing support!

---

Now, let your **Raspberry Pi 5** light up the room with **Pi5Neo**!

---

### 🔗 Useful Links
- [Pi5Neo on PyPI](https://pypi.org/project/Pi5Neo)
- [Pi5Neo GitHub Repository](https://github.com/vanshksingh/Pi5Neo)
- [Documentation](https://github.com/vanshksingh/Pi5Neo/wiki)
- [Raspberry Pi Official Website](https://www.raspberrypi.org)

