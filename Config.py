# All the configuration variables that are used by all the tests

import os

# Used only for the tests not directly testing power
DEFAULT_POWER = .2

# Com port/baud rate pairs for the input/output devices
LOAD_DEVICE = ("com1", 57600)
TUNE_DEVICE = ("com1", 57600)
FREQ_DEVICE = ("com1", 19200)

# Table D settings - this is where we load frequencies to test
TABLE_D = "input/table_d.csv"
D_HEADER_ROWS = 1
D_VSWR_COL = 0
D_FREQ_COL = 1
D_L_COL = 4
D_C_COL = 5
D_R_COL = 3

# Network analyzer data
NET_RES_FILE = "input/net.csv"
NET_RES_ROE_COL = 0
NET_RES_HEADER_ROWS = 6

# Table F Settings - Loading frequencies to test for Power Test
TABLE_F = "input/table_f.csv"
F_HEADER_ROWS = 1
F_ALL_POWERS_COL = 0
F_ALL_FREQS_COL = 1
