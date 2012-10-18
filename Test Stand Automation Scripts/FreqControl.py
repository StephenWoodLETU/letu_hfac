# This controls the frequency of the transmitter, as well as the power.

import time
import serial

# Local configuration variables
DEFAULT_FREQUENCY = 1995000
DEFAULT_POWER = 10

# Utilities for converting BCD to decimal and back
def _BCD_To_Int(bcdStr):
        """Convert a binary coded decimal to an integer."""
        val = 0
        multiplier = 1
        
        for curChar in bcdStr:
               
               # Decode first digit
               curVal = ord(curChar) & 0x0F
               val = val + multiplier * curVal
               multiplier *= 10
               
               # Add second digit
               curVal = ord(curChar) >> 4
               val = val + multiplier * curVal
               multiplier *= 10
               
        return val

def _Int_To_BCD(num,pad=0):
        """Convert an integer to a binary coded decimal to a string.  pad is the
        minimum length to make the string that will be returned."""
        val = int(num)
        toRet = b""
        
        while(val > 0):
               
               # Encode first digit
               curChar = (val % 10)
               val = val / 10
               
               # See if we have another digit to encode
               if(val > 0):
                     curChar = curChar | ((val % 10) << 4)
                     val = val / 10
                     
               # Append
               toRet = toRet + chr(curChar)
        
        # Pad response to a certain number of bytes
        for i in range(len(toRet),pad):
               toRet = toRet + '\0'
               
        return toRet

class FrequencyControl:
        
        def __init__(self, device):
               """Open a specific device as a frequency controller.  Device is
               a tuple with the first element being the com port on Windows or
               file name on Linux and the second element is the baud rate."""
               try:
                     self.device = device
                     self.comlink = serial.Serial(*device)
                     
                     # Send get ID
                     self._sendCommand(chr(0x19),chr(0x00))
                     self._readResponse(2)
                     
                     # Initialize to default settings
                     # LSB, Tx, RF power setting 20 of 255 - 1.995 MHz
                     
                     # Set RTTY
                     self._sendCommand(chr(0x01), chr(0x04))
                     
                     # Set to Tx
                     self._sendCommand(chr(0x1C), chr(0x00), chr(0x01))
                     
                     # Set RF power setting to 20
                     self._sendCommand(chr(0x14), chr(0x0A), _Int_To_BCD(DEFAULT_POWER, 1))
                     
                     # Set to default frequency
                     self.setFrequency(DEFAULT_FREQUENCY)
                     
               except:
                     print "Could not open ",device
                     raise

        # def __del__(self):
        
        def resetTuner(self):		
			   #set back down to normal?
               self._sendCommand(chr(0x14), chr(0x0A), _Int_To_BCD(2, 1))
               #set back to Rx?
               self._sendCommand(chr(0x1C), chr(0x00), chr(0x00))
			   #set to default frequency
               self.setFrequency(DEFAULT_FREQUENCY)
               self.comlink.close()

        def _sendCommand(self, command, subcommand=b'', data=b''):
               """Send a specific command to the device.  You must put the command,
               subcommand, and data into binary strings exactly how you want them
               sent."""
               line=b""
               
               # Create the output message
               line=line + chr(0xFE) + chr(0xFE) + chr(0x76) + chr(0xE0)
               
               line=line + command
               line=line + subcommand
               line=line + data
               
               line=line + chr(0xFD)
               
               self.comlink.write(line)
               self.comlink.flush()
               
               # Eat up the echoed command
               self.comlink.read(len(line))
               
        def _readResponse(self, responseDataLen):
               """Read a certain number of bytes back from the frequency
               device.  This value must include the length of the command,
               subcommand, and data that you want to read, and the returned
               string will be all of these concatenated to each other."""
               recvd = self.comlink.read(4+responseDataLen+1)
               return recvd[5:5+responseDataLen]
               
        def setFrequency(self, freq):
               "Set the frequency, in hertz, of the device."
               self._sendCommand(chr(0x05), data=_Int_To_BCD(freq,pad=5))
               self._readResponse(1)
               
        def readFrequency(self):
               "Read the frequency, in hertz, of the device."
               self._sendCommand(chr(0x03))
               return _BCD_To_Int(self._readResponse(6)[1:6])

        def setPower(self, power):
               "Set the radio frequency power to a certain value between 2 and 100 Watts."
               #val / 100 = hx / 0xff
               val = int((power/98)*0xff)
               self._sendCommand(chr(0x14), chr(0x0A), _Int_To_BCD(val, 1))
               #self._sendCommand(chr(0x14), chr(0x0A), chr(val))

        def setTx(self):
            self._sendCommand(chr(0x1C), chr(0x00), chr(0x01))
            
        def setRx(self):
            self._sendCommand(chr(0x1C), chr(0x00), chr(0x00))
            
        def getPower(self):
               pass
        
        def startTune(self):
               "Signals for the other device to tune"
               #set Rx
               self._sendCommand(chr(0x1C), chr(0x00), chr(0x00))
               #sent tune
               self._sendCommand(chr(0x1C), chr(0x01), chr(0x02))
               time.sleep(.2)
               #set Tx
               self._sendCommand(chr(0x1C), chr(0x00), chr(0x01))

# Main method to test the Frequency Controller.
if __name__ == '__main__':
        print("Testing FrequencyControl!")
        f = raw_input("Enter the device descriptor [com3]: ")
        b = int(raw_input("Enter the baud rate [19200]: "))
        
        print("Creating frequency controller")
        cont = FrequencyControl((f, b))
        
        print("Reading then setting frequency.")
        print 'Read the frequency: {}'.format(cont.readFrequency())
        print 'Now setting the frequency to 7 MHz'
        cont.setFrequency(7000000)
        print 'Read the new frequency: {}'.format(cont.readFrequency())
        print("Signaling for a tune")
        cont.startTune()
        #cont._sendCommand(chr(0x14), chr(0x0A), chr(0x80))
        print("Finished the tune")
        cont.setPower(20)
        print("Set the power")
        raw_input("All done. Ready to reset?")
        cont.resetTuner()

