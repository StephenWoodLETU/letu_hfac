# This controls the PowerMasterII for detecting VSWR
import crcmod.predefined

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
        
        calc_checksum = crcmod.predefined.mkCrcFun('crc-8')
            
    # def __del__(self):
    
    def _sendCommand(self, command) :
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
        
        self.comlink.write(line)
        self.comlink.flush()
        
    
    def getVSWR(self):
        # get the VSWR from the PM
        
        return 1