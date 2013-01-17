import socket
import time
import struct

class SCPI:
    PORT = 5025

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        self.f = self.s.makefile("rb")

        #RESET
        self.s.send("*RST\n")
        self.s.send("*CLS\n")

        #set output load
        self.s.send("OUTPut:LOAD INF\n")

    def getMeasurements(self):
      	self.s.send("R?\n")
        c = self.s.recv(1)
	    if c != "#":
	        print "*%s*"%(c,)
            return ""
        # read the number of digits that follow
        l = int(self.s.recv(1))
	    length = int(self.s.recv(l))

    	l = 0
	    r = ""
	    while l < int(length):
            c = self.s.recv(int(length)-l)
	        l += len(c)
	        r += c

	    # read the newline character
	    self.s.recv(1)

	    m = struct.unpack(">%dd"%(int(length)/8,), r)

	    return m

