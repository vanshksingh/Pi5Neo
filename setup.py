# setup.py
from setuptools import setup, find_packages

setup(
    name='Pi5Neo',
    version='1.0.3',
    description='A NeoPixel LED control library for Raspberry Pi 5 using SPI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vansh Kumar Singh',
    author_email='vsvsasas@gmail.com',
    url='https://github.com/vanshksingh/pi5neo',  # Your GitHub URL
    packages=find_packages(),
    install_requires=[
        'spidev',  # Only include spidev as a requirement
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',  # Specifying Linux for Raspberry Pi
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='raspberrypi5, neopixel, spi, led-strip, hardware',  # Keywords to improve searchability
    platforms=['Raspberry Pi 5', 'Equivalent Raspberry Pi boards'],
    python_requires='>=3.6',
)
