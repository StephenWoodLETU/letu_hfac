# This controls the PowerMasterII for detecting VSWR
import serial
import time
from customCrc import *
import Config

class PMControl:
    def __init__(self, device):
        """Open a device (linux file) to communicate with to control
        the PowerMaster (PM)"""
        try:
            self.device = device
            self.comlink = serial.Serial(*device)
            
        except:
            print("Could not open ", device)
            raise
        
        
    # def __del__(self):
    
    def sendCommand(self, command) :
        """Send a specific command to the device.  You must put the command,
        into binary strings exactly how you want it sent sent."""
        
        line=b""
       
        # Add the STX to the beggining of the message
        line = chr(0x02)
        # Add the payload to the message
        line = line + command
        # Add the ETX after the payload
        line = line + chr(0x03)
        # Add the checksum
        line = line + calcCrc(command)

        # Finalize the message with a carriage return
        line = line + chr(0x0D)
        
        # Print out the message in Hex format:
        # print('Command: ' + " $".join("{0:x}".format(ord(c)) for c in line))

        self.comlink.write(line)
        #print('Recieved: ' + self.comlink.readline())
        self.comlink.flush()
    
    def startRealTimeData(self):
        # Report every 140 ms
        self.sendCommand('D3')

    def readRealTimeVswr(self):
        response = self.comlink.readline()
        while response[1] != 'D':
            response = self.comlink.readline()
        splitResponse = response.split(',')
        vswr = splitResponse[3]
        return vswr

    def stopRealTimeData(self):
        self.sendCommand('D0')
        self.comlink.flushInput()

    def getVSWR(self):
        # get the VSWR from the PM
        self.sendCommand('D5')
        
        # Eat up the superfulous responses...
        response = self.comlink.readline()
        while response[1] != 'D' :
            response = self.comlink.readline()
        splitResponse = response.split(',')
        vswr = splitResponse[3]
        self.comlink.flushInput()
        return vswr

    def getResponse(self):
        response = self.comlink.readline()
        self.comlink.flush()
        return response



if __name__ == '__main__':
    keepGoing = 'y'
    while keepGoing == 'y':
        print("Testing the PM control interface")
        
        com = PMControl(Config.PM_DEVICE)

        #userCommand = raw_input("Command to send: ")
        #com.sendCommand(userCommand)
        #response = com.getResponse()
        #print response
        com.startRealTimeData()
        for i in range(0,10):
            print (com.readRealTimeVswr())
        com.stopRealTimeData()
        keepGoing = raw_input("Keep going? [y/n]: ")
