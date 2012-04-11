# All the configuration variables that are used by all the tests

import os

# Used only for the tests not directly testing power
DEFAULT_POWER = .2

# Com port/baud rate pairs for the input/output devices
LOAD_DEVICE = ("com1", 57600)
TUNE_DEVICE = ("com1", 57600)
FREQ_DEVICE = ("com1", 19200)

#output files
TuneTestoutput = "TuneTestOutput.csv"
TunePowerTestoutput = "TunePowerTestOutput.csv"
PowerTestoutput = "PowerTestOutput.csv"

# Network analyzer data
NET_RES_FILE = "input/net.csv"
NET_RES_ROE_COL = 1
NET_RES_HEADER_ROWS = 6

# Table F Settings - Loading frequencies to test for Power Test
TABLE_F = "input/table_f.csv"
F_HEADER_ROWS = 1
F_ALL_POWERS_COL = 0
F_ALL_FREQS_COL = 1

#PowerTest data
TABLE_J = "input/table_j.csv"
J_HEADER_ROWS = 3
J_FREQ_COL = 0
J_LOADS_PER_VSR = 6
J_VSRS = 5
J_R_COL = 3
J_L_COL = 4
J_C_COL = 5

