# This controls the PowerMasterII for detecting VSWR
import serial
import time
import crcmod.predefined

class PMControl:
    def __init__(self, device, crcType):
        """Open a device (linux file) to communicate with to control
        the PowerMaster (PM)"""
        try:
            self.device = device
            self.comlink = serial.Serial(*device)
            
        except:
            print("Could not open ", device)
            raise
        
        self.calc_checksum = crcmod.predefined.mkCrcFun(crcType)
        
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
        line = line + hex(self.calc_checksum(command))
        # Finalize the message with a carriage return
        line = line + chr(0x0D)
        
        print('Command: ', line)

        self.comlink.write(line)
        print('Recieved: ', self.comlink.readline())
        self.comlink.flush()
        
    
    def getVSWR(self):
        # get the VSWR from the PM
        
        return 1

if __name__ == '__main__':
    print("Testing the PM control interface")
    
    for i in range(0,7) :
        crcType = raw_input("Enter the CRC: ")
        com = PMControl(('/dev/ttyUSB0', 38400), crcType)

        print("Tring to set display intensity to 0")
        com.sendCommand('I2')
        print("Done")
