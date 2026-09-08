"""
pi5neo/pi5neo.py — NeoPixel driver for Raspberry Pi 5 via SPI.
"""

import spidev
import time
import warnings
import functools
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class EPixelType(Enum):
    """Supported NeoPixel color channel orderings."""
    RGB = 'RGB'
    GRB = 'GRB'
    RGBW = 'RGBW'
    GRBW = 'GRBW'


@dataclass
class LEDColor:
    """Represents an RGB or RGBW color value (0–255 per channel)."""
    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 0


def _deprecated(reason: str):
    """Decorator to mark functions as deprecated with a custom message."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated: {reason}",
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Precomputed SPI encoding for NeoPixel protocol bits
_BIT_HIGH = 0xFC
_BIT_LOW = 0xC0


class Pi5Neo:
    """Drive WS2812 / SK6812 NeoPixel strips from a Raspberry Pi 5 over SPI."""

    def __init__(
        self,
        spi_device: str = '/dev/spidev0.0',
        num_leds: int = 10,
        spi_speed_khz: int = 800,
        pixel_type: EPixelType = EPixelType.GRB,
        quiet_mode: bool = False,
        preamble_bytes: int = 0
    ):
        self.num_leds = num_leds
        self.pixel_type = pixel_type
        self.quiet_mode = quiet_mode
        self.preamble_bytes = preamble_bytes
        self.spi_speed = spi_speed_khz * 1024 * 8

        self.spi = spidev.SpiDev()

        if pixel_type in (EPixelType.RGB, EPixelType.GRB):
            self.bytes_per_led = 24  # 3 channels × 8 bits
        elif pixel_type in (EPixelType.RGBW, EPixelType.GRBW):
            self.bytes_per_led = 32  # 4 channels × 8 bits
        else:
            raise ValueError(f"Invalid pixel_type: {pixel_type!r}")

        self.raw_data = [0] * (self.preamble_bytes + self.num_leds * self.bytes_per_led)

        # Each LED gets its own LEDColor instance (avoids shared-reference bug)
        self.led_state: list[LEDColor] = [LEDColor() for _ in range(self.num_leds)]

        if self.open_spi_device(spi_device):
            time.sleep(0.1)
            self.clear_strip()
            self.update_strip()

    # ------------------------------------------------------------------
    # SPI helpers
    # ------------------------------------------------------------------

    def open_spi_device(self, device_path: str) -> bool:
        """Open the SPI device at *device_path* (e.g. '/dev/spidev0.0')."""
        try:
            bus, device = map(int, device_path.split("spidev")[-1].split('.'))
            self.spi.open(bus, device)
            self.spi.max_speed_hz = self.spi_speed
            if not self.quiet_mode:
                print(f"Opened SPI device: {device_path}")
            return True
        except Exception as e:
            if not self.quiet_mode:
                print(f"Failed to open SPI device: {e}")
            return False

    def close(self) -> None:
        """Close the SPI device and release resources."""
        try:
            self.spi.close()
        except Exception:
            pass

    def send_spi_data(self) -> None:
        """Transmit the raw bitstream buffer to the strip via SPI."""
        self.spi.xfer3(self.raw_data)

    # ------------------------------------------------------------------
    # Bit-level encoding
    # ------------------------------------------------------------------

    @staticmethod
    def byte_to_bitstream(byte: int) -> list[int]:
        """Encode a single byte into 8 NeoPixel SPI timing values."""
        return [_BIT_HIGH if (byte & (1 << (7 - i))) else _BIT_LOW for i in range(8)]

    def color_to_spi_bitstream(
        self,
        pixel_type: EPixelType,
        red: int,
        green: int,
        blue: int,
        white: int = 0,
    ) -> list[int]:
        """Convert colour channels to a full NeoPixel SPI bitstream
        ordered according to *pixel_type*."""
        r = self.byte_to_bitstream(red)
        g = self.byte_to_bitstream(green)
        b = self.byte_to_bitstream(blue)
        w = self.byte_to_bitstream(white)

        order = {
            EPixelType.RGB:  (r, g, b),
            EPixelType.GRB:  (g, r, b),
            EPixelType.RGBW: (r, g, b, w),
            EPixelType.GRBW: (g, r, b, w),
        }

        return [bit for group in order[pixel_type] for bit in group]

    # Keep around for backwards compat, but steer users to the unified method.

    @_deprecated("Use color_to_spi_bitstream() instead")
    def rgb_to_spi_bitstream(self, red, green, blue):
        return self.color_to_spi_bitstream(EPixelType.GRB, red, green, blue)

    @_deprecated("Use color_to_spi_bitstream() instead")
    def rgbw_to_spi_bitstream(self, red, green, blue, white):
        return self.color_to_spi_bitstream(EPixelType.GRBW, red, green, blue, white)

    # ------------------------------------------------------------------
    # Public LED API
    # ------------------------------------------------------------------

    def clear_strip(self) -> None:
        """Turn off every LED (sets all channels to 0)."""
        self.fill_strip(0, 0, 0, 0)

    def fill_strip(self, red: int = 0, green: int = 0, blue: int = 0, white: int = 0) -> None:
        """Set every LED on the strip to the same colour."""
        self.led_state = [LEDColor(red, green, blue, white) for _ in range(self.num_leds)]

    def set_led_color(self, index: int, red: int, green: int, blue: int, white: int = 0) -> bool:
        """Set the colour of a single LED by index. Returns False if index is out of range."""
        if 0 <= index < self.num_leds:
            self.led_state[index] = LEDColor(red, green, blue, white)
            return True
        return False

    def set_led_color_object(self, index: int, color: LEDColor) -> bool:
        """Set a single LED's colour using an LEDColor instance."""
        if 0 <= index < self.num_leds:
            self.led_state[index] = LEDColor(color.red, color.green, color.blue, color.white)
            return True
        return False

    def get_led_color(self, index: int) -> Optional[LEDColor]:
        """Return the current LEDColor for *index*, or None if out of range."""
        if 0 <= index < self.num_leds:
            c = self.led_state[index]
            return LEDColor(c.red, c.green, c.blue, c.white)
        return None

    def update_strip(self, sleep_duration: Optional[float] = 0.1) -> None:
        """Flush the current LED state to the physical strip via SPI.

        Parameters
        ----------
        sleep_duration : float or None
            Seconds to wait after transmission (gives the strip time to latch).
            Pass ``None`` to skip the delay.
        """
        idx = self.preamble_bytes
        for led in self.led_state:
            bitstream = self.color_to_spi_bitstream(
                self.pixel_type, led.red, led.green, led.blue, led.white
            )
            self.raw_data[idx:idx + self.bytes_per_led] = bitstream
            idx += self.bytes_per_led

        self.send_spi_data()

        if sleep_duration is not None:
            time.sleep(sleep_duration)

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_strip()
        self.update_strip(sleep_duration=None)
        self.close()
        return False

