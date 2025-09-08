# pi5neo/pi5neo.py
import spidev
import time
from enum import Enum

class EPixelType(Enum):
    RGB = "RGB"
    RGBW = "RGBW"

class LEDColor:
    """Represents an RGB or RGBW color for the NeoPixels"""

    def __init__(self, red=0, green=0, blue=0, white=0):
        self.red = red
        self.green = green
        self.blue = blue
        self.white = white

class Pi5Neo:
    def __init__(
        self,
        spi_device="/dev/spidev0.0",
        num_leds=10,
        max_brightness=100,
        spi_speed_khz=800,
        pixel_type=EPixelType.RGB,
        quiet_mode=False,
    ):
        """Initialize the Pi5Neo class with SPI device, number of LEDs, speed, pixel type, and optional quiet mode"""
        self.num_leds = num_leds
        self.max_brightness = (
            max_brightness if (max_brightness >= 0 and max_brightness <= 100) else 100
        ) / 100
        self.pixel_type = pixel_type
        self.quiet_mode = quiet_mode
        self.spi_speed = spi_speed_khz * 1024 * 8  # Convert kHz to bytes per second
        self.spi = spidev.SpiDev()  # Create SPI device instance

        # Determine bytes per LED based on pixel_type
        self.pixel_type = pixel_type
        if self.pixel_type is EPixelType.RGB:
            self.bytes_per_led = 24  # 3 channels * 8 bits/channel
        elif self.pixel_type is EPixelType.RGBW:
            self.bytes_per_led = 32  # 4 channels * 8 bits/channel
        else:
            raise ValueError("Invalid pixel_type. Must be one of EPixelType.")

        self.raw_data = [0] * (
            self.num_leds * self.bytes_per_led
        )  # Placeholder for raw data sent via SPI
        self.led_state = [
            LEDColor()
        ] * self.num_leds  # Initial state for each LED (off)

        # Open the SPI device
        if self.open_spi_device(spi_device, quiet_mode):
            time.sleep(0.1)  # Short delay to ensure device is ready
            self.clear_strip()  # Clear the strip on startup
            self.update_strip()

    def open_spi_device(self, device_path, quiet_mode):
        """Open the SPI device with the provided path"""
        try:
            bus, device = map(int, device_path[-3:].split("."))
            self.spi.open(bus, device)
            self.spi.max_speed_hz = self.spi_speed
            if quiet_mode == False:
                print(f"Opened SPI device: {device_path}")
            return True
        except Exception as e:
            if quiet_mode == False:
                print(f"Failed to open SPI device: {e}")
            return False

    def send_spi_data(self):
        """Send the raw data buffer to the NeoPixel strip via SPI"""
        spi_message = bytes(self.raw_data)
        self.spi.xfer3(list(spi_message))  # previously spi.xfer2

    def bitmask(self, byte, position):
        """Retrieve the value of a specific bit in a byte"""
        return bool(byte & (1 << (7 - position)))

    def byte_to_bitstream(self, byte):
        """Convert a byte to the NeoPixel timing bitstream"""
        bitstream = [0xC0] * 8  # Initialize with LOW bits
        for i in range(8):
            if self.bitmask(byte, i):
                bitstream[i] = 0xF8  # Set HIGH bits for '1'
        return bitstream

    def rgb_to_spi_bitstream(self, red, green, blue):
        """Convert RGB values to the NeoPixel bitstream format for SPI"""
        green_bits = self.byte_to_bitstream(green)  # Send green first
        red_bits = self.byte_to_bitstream(red)  # Then red
        blue_bits = self.byte_to_bitstream(blue)  # Then blue
        return green_bits + red_bits + blue_bits  # Concatenate GRB order

    def rgbw_to_spi_bitstream(self, red, green, blue, white):
        """Convert RGBW values to the NeoPixel bitstream format for SPI (GRBW order)"""
        green_bits = self.byte_to_bitstream(green)  # Send green first
        red_bits = self.byte_to_bitstream(red)  # Then red
        blue_bits = self.byte_to_bitstream(blue)  # Then blue
        white_bits = self.byte_to_bitstream(white)  # Then white
        return green_bits + red_bits + blue_bits + white_bits  # Concatenate GRBW order

    def clear_strip(self):
        """Turn off all LEDs on the strip"""
        self.fill_strip(0, 0, 0, 0)

    def fill_strip(self, red=0, green=0, blue=0, white=0):
        """Fill the entire strip with a specific color"""
        color = LEDColor(red, green, blue, white)
        self.led_state = [color] * self.num_leds  # Set all LEDs to the same color

    def set_led_color(self, index, red, green, blue, white=0):
        """Set the color of an individual LED"""
        if 0 <= index < self.num_leds:
            self.led_state[index] = LEDColor(red, green, blue, white)
            return True
        return False

    def update_strip(self, sleep_duration=0.1):
        """Send the current state of the LED strip to the NeoPixels
        Parameters: - sleep_duration (float): The duration (in seconds) to pause after sending the data.
        If None, no delay is introduced.
        """
        total_bytes = 0
        for i in range(self.num_leds):
            led = self.led_state[i]  # Get the color for each LED
            max_red = int(led.red * self.max_brightness)
            max_green = int(led.green * self.max_brightness)
            max_blue = int(led.blue * self.max_brightness)
            if self.pixel_type is EPixelType.RGB:
                bitstream = self.rgb_to_spi_bitstream(max_red, max_green, max_blue)
            elif self.pixel_type is EPixelType.RGBW:
                max_white = int(led.white * self.max_brightness)
                bitstream = self.rgbw_to_spi_bitstream(
                    max_red, max_green, max_blue, max_white
                )

            for j in range(self.bytes_per_led):
                self.raw_data[total_bytes] = bitstream[j]
                total_bytes += 1
        self.send_spi_data()

        if sleep_duration is not None:
            time.sleep(sleep_duration)
