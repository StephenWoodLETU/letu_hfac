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
PM_DEVICE   = ('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400gmLr-if00-port0', 19200)
LOAD_DEVICE = ('/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_649363331373519161C1-if00', 19200)
ICOM_DEVICE = ('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_IC-7200_0202227-if00-port0', 38400)

#output files
TestOutputFile = "TestResults.csv"

# Input files settings
VAR_LOAD_COMBOS = "input/loadCombinations.csv"
VLC_HEADER_ROWS = 1
POWER_AND_FREQ = "input/powers.csv"

# Requirements
MAX_TUNE_TIME = 5
MAX_VSWR = 2.0
