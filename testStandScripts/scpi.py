import socket
import time
import struct

class SCPI:
    PORT = 5025

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
    
    def getResponse(self):
        responseChar = ''
        responseStr = ''
        while responseChar != '\n' :
            responseChar = self.s.recv(1)
            responseStr = responseStr + responseChar
        return responseStr

    def setScreen(self, isOn):
        self.s.send("DISP:ENABLE %d" % isOn)

    def getMagAndPhase(self):
        # Set the trace
        self.s.send("CALC:PAR1:DEF S11;*OPC?\n")
        self.getResponse()
        
        # Set the format to get magnitude
        self.s.send("CALC1:FORM MLIN;*OPC?\n")
        self.getResponse()

        # Select the trace
        self.s.send("CALC:PAR1:SEL;*OPC?\n")
        self.getResponse()

	
        # Set to single read (wait for response)
        self.s.send("INIT:CONT OFF\n")
        self.s.send("INIT:IMM;*OPC?\n")
        # Wait for response
        self.getResponse()

        # Get the magnitude
        self.s.send("CALC:MARK1:Y?\n")
        magStr = self.getResponse()

        # Set format to get phase
        self.s.send("CALC1:FORM PHAS;*OPC?\n")
        self.getResponse()

        # Get the phase
        self.s.send("CALC:MARK1:Y?\n")
        phaseStr = self.getResponse()
        		
        # Check for errors (0 is no error)
        self.s.send("SYST:ERR?\n")
        error = self.getResponse()
        
        mag = self.strToNum(magStr)
        phase = self.strToNum(phaseStr)
        
        return (mag,phase)
		
    def strToNum(self, string):
        (value,garbage) = string.split(',')
        (num,exp) = value.split('E')
        finalNumber = float(num) * pow(10,int(exp))
        return finalNumber

if __name__ == '__main__':
    print("Testing SCPI control")

    ip = "10.52.88.137"

    scpi = SCPI(ip)
    (mag,phase) = scpi.getMagAndPhase()
    print("The magnitude is: {}".format(mag))
    print("The phase is: {}".format(phase)) 
    (mag,phase) = scpi.getMagAndPhase()
    print("The magnitude is: {}".format(mag))
    print("The phase is: {}".format(phase)) 
    (mag,phase) = scpi.getMagAndPhase()
    print("The magnitude is: {}".format(mag))
    print("The phase is: {}".format(phase)) 
    (mag,phase) = scpi.getMagAndPhase()
    print("The magnitude is: {}".format(mag))
    print("The phase is: {}".format(phase)) 

