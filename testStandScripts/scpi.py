import socket
import time
import struct

class SCPI:
    PORT = 5025

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        #self.f = self.s.makefile("rb")

        #RESET
        #self.s.send("*RST\n")
        #self.s.send("*CLS\n")

        #set output load
        #self.s.send("OUTPut:LOAD INF\n")

    def setScreen(self, isOn):
        self.s.send("DISP:ENABLE %d" % isOn)


    def getMagAndPhase(self):
      # Set the trace
      	self.s.send("CALC:PAR1:DEF S11")
        
		# Set the format to get magnitude
        self.s.send("CALC1:FORM MLIN")
		
		# Select the trace
      	self.s.send("CALC:PAR1:SEL")
		
		# Set to single read (wait for response)
      	self.s.send("INIT:CONT OFF")
      	self.s.send("INIT:IMM;*OPC?")
		# Wait for response
        self.s.recv(1)
		
		# Get the magnitude
      	self.s.send("CALC:MARK1:Y?")
        magStr = self.s.recv(15)
		
		# Set format to get phase
      	self.s.send("CALC1:FORM PHAS")
		
		# Get the phase
      	self.s.send("CALC:MARK1:Y?")
        phaseStr = self.s.recv(15)
        		
        # Check for errors (0 is no error)
        self.s.send("SYST:ERR?")
        error = self.s.recv(1)
        
        mag = strToNum(magStr)
        phase = strToNum(phaseStr)
        
        return (mag,phase)
		
    def strToNum(self s, string):
        valueTupple = string.split(',')
        (num,exp) = valueTupple(1).split('E+')
        finalNumber = num * 10^exp
        return finalNumber

if __name__ == '__main__':
    print("Testing SCPI control")

    ip = "10.52.88.137"

    scpi = SCPI(ip)
    (mag,phase) = scpi.getMagAndPhase()
    print "The magnitude is: " mag
    print "The phase is: " phase	

