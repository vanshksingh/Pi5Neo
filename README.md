# Pi5Neo

### Simplifying NeoPixel LED Control on Raspberry Pi 5 via SPI (GPIO 10)

[![PyPI version](https://badge.fury.io/py/Pi5Neo.svg)](https://badge.fury.io/py/Pi5Neo)
[![Python Versions](https://img.shields.io/pypi/pyversions/Pi5Neo.svg)](https://pypi.org/project/Pi5Neo)
[![License](https://img.shields.io/github/license/vanshksingh/Pi5Neo)](LICENSE)

![IMG_7596](https://github.com/user-attachments/assets/6fb727ae-789e-4d25-9dd7-38599fdbb81e)

Pi5Neo is a Python library for controlling **NeoPixel LED strips** on the **Raspberry Pi 5** (or equivalent boards) over the **SPI interface**. It supports both RGB (WS2812B) and RGBW (SK6812) strips, exposes a clean context-manager API, and ships with a growing set of ready-to-run examples.

---

## What's New in v1.1.0

- **RGBW / SK6812 support** — new `EPixelType` enum (`RGB`, `GRB`, `RGBW`, `GRBW`) lets you select the exact channel order for your strip hardware.
- **`LEDColor` dataclass** — represent colors as structured objects; read back any LED's current state with `get_led_color()`.
- **`set_led_color_object()` / `get_led_color()`** — object-oriented helpers alongside the existing index-based API.
- **Context-manager support** — `with Pi5Neo(...) as neo:` guarantees the strip is cleared and SPI is released on exit, even after exceptions.
- **`quiet_mode` parameter** — suppress all console output for production scripts.
- **Configurable `update_strip` delay** — pass `sleep_duration=None` to skip the latch delay, or any float for custom timing.
- **Reorganised examples** — split into `basic/`, `animations/`, and `effects/` sub-directories with clean, well-commented scripts.
- **Deprecated helpers** — `rgb_to_spi_bitstream()` and `rgbw_to_spi_bitstream()` now emit `DeprecationWarning`; use `color_to_spi_bitstream()` instead.

---

## Key Features

- **RGB and RGBW support** — WS2812B (GRB) and SK6812 (RGBW/GRBW) out of the box.
- **`LEDColor` dataclass** — structured colour values with per-channel access.
- **Context-manager API** — automatic cleanup with `with` statements.
- **Quiet mode** — silence all print output for daemon/production use.
- **Smooth animations** — rainbow, breathing, comet, meteor, fireworks, theater chase, and more.
- **Minimal dependencies** — only `spidev` required.
- **High LED count support** — configurable kernel SPI buffer for 170+ LEDs.

---

## Installation

```bash
pip install pi5neo
```

### Requirements

- Python 3.6+
- `spidev` (installed automatically)

### Hardware

- Raspberry Pi 5 (or equivalent board with SPI)
- NeoPixel LED strip — WS2812B (RGB/GRB) or SK6812 (RGBW/GRBW)

---

## Setup: Enable SPI

```bash
sudo raspi-config
# → 3 Interface Options → I4 SPI → Yes
```

---

## Quick Start

```python
from pi5neo import Pi5Neo

# Initialize with 10 LEDs at 800 kHz on /dev/spidev0.0
neo = Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800)

neo.fill_strip(255, 0, 0)   # Red
neo.update_strip()

neo.set_led_color(4, 0, 0, 255)  # Blue on LED #5
neo.update_strip()
```

### Context Manager (recommended)

The strip is always cleared and SPI released on exit, even if an exception occurs:

```python
from pi5neo import Pi5Neo

with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    neo.fill_strip(0, 255, 0)   # Green
    neo.update_strip()
    # SPI closed and strip cleared automatically here
```

### RGBW / SK6812 Strips

```python
from pi5neo import Pi5Neo, EPixelType

with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800,
            pixel_type=EPixelType.GRBW, quiet_mode=True) as neo:
    neo.fill_strip(0, 0, 0, 255)   # White channel only
    neo.update_strip()
```

### LEDColor Objects

```python
from pi5neo import Pi5Neo, LEDColor

with Pi5Neo('/dev/spidev0.0', num_leds=10, spi_speed_khz=800, quiet_mode=True) as neo:
    color = LEDColor(red=255, green=128, blue=0)
    neo.set_led_color_object(0, color)
    neo.update_strip()

    # Read the current colour of any LED
    current = neo.get_led_color(0)
    print(current)   # LEDColor(red=255, green=128, blue=0, white=0)
```

---

## API Reference

### `Pi5Neo(spi_device, num_leds, spi_speed_khz, pixel_type, quiet_mode)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `spi_device` | `str` | `'/dev/spidev0.0'` | SPI device path |
| `num_leds` | `int` | `10` | Number of LEDs in the strip |
| `spi_speed_khz` | `int` | `800` | SPI clock speed in kHz |
| `pixel_type` | `EPixelType` | `EPixelType.GRB` | Channel order — `RGB`, `GRB`, `RGBW`, or `GRBW` |
| `quiet_mode` | `bool` | `False` | Suppress all console output |

### Methods

| Method | Description |
|---|---|
| `fill_strip(r, g, b, w=0)` | Set every LED to the same colour |
| `set_led_color(index, r, g, b, w=0)` | Set a single LED by index |
| `set_led_color_object(index, LEDColor)` | Set a single LED using an `LEDColor` instance |
| `get_led_color(index)` | Return the current `LEDColor` for an LED (copy) |
| `clear_strip()` | Turn off all LEDs |
| `update_strip(sleep_duration=0.1)` | Flush state to the strip; pass `None` to skip latch delay |
| `close()` | Close the SPI device |

### `EPixelType`

| Value | Strip type |
|---|---|
| `EPixelType.GRB` | WS2812B (most common) |
| `EPixelType.RGB` | Some RGB strips |
| `EPixelType.GRBW` | SK6812 RGBW (GRB channel order) |
| `EPixelType.RGBW` | SK6812 RGBW (RGB channel order) |

### `LEDColor`

```python
from pi5neo import LEDColor

c = LEDColor(red=255, green=0, blue=128, white=0)
```

All fields default to `0`. The `white` field is only used with RGBW pixel types.

---

## Examples

Examples are organized under the `examples/` directory:

```
examples/
├── basic/
│   ├── example_usage.py      # Solid color + rainbow cycle
│   ├── single_led.py         # Single LED control
│   ├── random_blink.py       # Random blinking LEDs
│   ├── pixel_types.py        # EPixelType demo (RGB / RGBW)
│   ├── led_color_object.py   # LEDColor dataclass + color shifting
│   └── context_manager.py    # Context manager / safe cleanup
├── animations/
│   ├── breath.py             # Breathing / pulse effect
│   ├── fade.py               # Fade in / fade out
│   ├── smooth_fade.py        # Cosine smooth fade
│   ├── rainbow.py            # Rainbow wave
│   └── thinking.py           # "Thinking" spinner animation
└── effects/
    ├── comet.py              # Comet tail
    ├── meteor.py             # Meteor shower
    ├── firework.py           # Firework burst
    ├── knight_rider.py       # Knight Rider scanner
    ├── snake.py              # Snake crawl
    ├── ripple.py             # Ripple effect
    ├── twinkle.py            # Random twinkle
    ├── loading.py            # Loading bar
    ├── colour_bounce.py      # Colour bounce
    └── theater_chase.py      # Theater chase
```

---

## Driving High LED Counts

The default `spidev` kernel buffer is 4096 bytes, which supports up to ~170 LEDs. For larger strips, increase the buffer by appending to the single line in `/boot/firmware/cmdline.txt` and rebooting:

```
spidev.bufsiz=32768
```

For RGBW strips the per-LED byte cost is higher (32 bytes vs. 24), so adjust accordingly.

---

## Contributing

1. Fork the repo.
2. Create a branch: `git checkout -b my-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push: `git push origin my-feature`
5. Open a Pull Request.

Issues and feature requests are welcome!

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

Pi5Neo was inspired by various open-source NeoPixel and SPI projects. Thanks to all contributors and to the maintainers of `spidev` and the Raspberry Pi ecosystem.

---

### Useful Links

- [Pi5Neo on PyPI](https://pypi.org/project/Pi5Neo)
- [Pi5Neo GitHub Repository](https://github.com/vanshksingh/Pi5Neo)
- [Raspberry Pi Official Website](https://www.raspberrypi.org)