# All the configuration variables that are used by all the tests

import os

# Set to true if this test will be attended
ATTENDED_TEST = True

# Set to true if using a competitor's coupler
# If true, the Arduino coupler interface will not be used
COMPETITOR_TUNER = True

# Set how to communicate with the load Arduino.
# Options are: usb, fake, or i2c
LOAD_IFACE = 'usb'

# Com port/baud rate pairs for the input/output devices
#! Change these for RasPi
PM_DEVICE   = ('/home/pi/serial/ttyPM', '38400')
LOAD_DEVICE = ('/home/pi/serial/ttyARD', '9600')
ICOM_DEVICE = ('/home/pi/serial/ttyICOM', '19200')

#output files
TestOutputFile = "TestResults.csv"

# Input files settings
VAR_LOAD_COMBOS = "input/loadCombinations.csv"
VLC_HEADER_ROWS = 1
POWER_AND_FREQ = "input/powers.csv"

# Requirements
MAX_TUNE_TIME = 5
MAX_VSWR = 1.6
