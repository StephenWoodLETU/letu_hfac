# All the configuration variables that are used by all the tests

import os

# Set to true if this test will be attended
ATTENDED_TEST = True

# Set to true if using a competitor's coupler
# If true, the Arduino coupler interface will not be used
COMPETITOR_TUNER = True

# Set how to communicate with the load Arduino.
# Options are: usb, fake, or i2c
LOAD_IFACE = 'fake'

# Com port/baud rate pairs for the input/output devices
#! Change these for RasPi
LOAD_DEVICE = ("/dev/ttyACM0", 19200)
ICOM_DEVICE = ("/dev/ttyUSB0", 19200)
PM_DEVICE   = ('/dev/ttyUSB1', 38400)

#output files
TestOutputFile = "TestResults.csv"

# Input files settings
VAR_LOAD_COMBOS = "input/loadCombinations.csv"
VLC_HEADER_ROWS = 1
POWER_AND_FREQ = "input/powers.csv"

# Requirements
MAX_TUNE_TIME = 5
MAX_VSWR = 2.0
