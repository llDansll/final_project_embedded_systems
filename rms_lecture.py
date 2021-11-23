#!/bin/python3

"""
        Application to know the power value rms of a particular load

        Author: Daniel M. Barrera Leguizamón
"""

import time                                                     # Import library for delays
import board                                                    # Import ports
import busio                                                    # Import I2C protocole
import Adafruit_ADS1x15                                         # Import the ADS1x15 module.
from Adafruit_IO import *                                       # Import library to link the AdafruitIO Platform and Raspberry Pi 3
aio = Client('llDansll','aio_nDrD87XzusllYqmkpgUEFK0xj4dp')     # User and key synchronization

adc = Adafruit_ADS1x15.ADS1115()                                # Create an ADS1115 ADC (16-bit) instance.
GAIN = 1                                                        # GAIN - 1 = +/-4.096V

data_01 = []
data_02 = []
voltage = 0
current = 0
vrms = 0.0
irms = 0.0
power = 0.0

while 1:

    for i in range(100):                                                                        # Take 100 samples
        data_01.append((adc.read_adc(0,gain=GAIN, data_rate=860)*(4.096/32767.0)) - 1.67)       # Obtain the analog value from pin A0 (voltage)
        data_02.append((adc.read_adc(1,gain=GAIN, data_rate=860)*(4.096/32767.0)) - 2.5)        # Obtain the analog value from pin A1 (current
    i = 0
    for j in range(100):                                                                        # Obtain the squared value of current and voltage until 100 samples
        voltage = voltage + pow(data_01[j],2)
        current = current + pow(data_02[j],2)
    j = 0

    vrms = pow(voltage/100,0.5) * (510/3.85)                                                    # Obtain the real current and voltage rms value
    irms = pow(current/100,0.5) / 0.185                                                         # taking into account the gain of both sensors

    data_01.clear()                                                                             # Clear the value storage in the vector
    data_02.clear()                                                                             # Clear the value storage in the vector
    voltage = 0                                                                                 # Clear variable voltage
    current = 0                                                                                 # Clear variable current

    if (vrms <= 0.6 and irms <= 0.04):                                                          # If the voltage and current are very small, the values will
        vrms = 0                                                                                # be assigned as zero
        irms = 0

    power = vrms*irms                   # Calculate power

    aio.send("vrms",vrms)               # Send rms voltage to AdafruitIO Platform
    aio.send("irms",irms)               # Send rms current to AdafruitIO Platform
    aio.send("power",power)             # Send power to AdafruitIO Platform

    time.sleep(10)                      # Delay of ten seconds