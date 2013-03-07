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
LOAD_DEVICE = ("com7", 19200)
ICOM_DEVICE = ("com3", 19200)
FREQ_DEVICE = ("com3", 19200)
PM_DEVICE = ('/dev/ttyUSB0', 38400)

#output files
TestOutputFile = "TestResults.csv"

# Input files settings
VAR_LOAD_COMBOS = "input/loadCombinations.csv"
VLC_HEADER_ROWS = 1
POWER_AND_FREQ = "input/powers.csv"

#PowerTest data
TABLE_J = "input/table_j.csv"
J_HEADER_ROWS = 3
J_FREQ_COL = 0
J_LOADS_PER_VSR = 6
J_VSRS = 5
J_R_COL = 2
J_L_COL = 3
J_C_COL = 4

