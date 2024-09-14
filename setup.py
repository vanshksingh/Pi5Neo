# setup.py
from setuptools import setup, find_packages

setup(
    name='Pi5Neo',
    version='1.0.0',
    description='A NeoPixel LED control library for Raspberry Pi 5 using SPI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vansh Kumar Singh',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/pi5neo',
    packages=find_packages(),
    install_requires=[
        'spidev',
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
