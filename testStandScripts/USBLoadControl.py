# This file communicates with the load Arduino.
# The format for this is:
#  setup by sending "R L C;"
#  reset by sending "<char>"

from LoadControl import LoadControl
import time
import serial 
import Config

class USBLoadControl(LoadControl):
        
        def __init__(self, device):
               """Open a specific device as a load controller.  Device is
               a tuple with the first element being the com port on Windows or
               file name on Linux and the second element is the baud rate."""
               try:
                     self.device = device
                     self.comlink = serial.Serial(*device)
               except:
                     print("Could not open ",device)
                     raise
        
        def __del__(self):
               self.comlink.close()

        def setRLC(self, r, l, c):
               # Format is R L C;
               command = b"{0} {1} {2};".format(r,l,c)
               self.comlink.write(command)
               self.comlink.flush()

        def reset(self):
               # Format is <char>
               self.comlink.write(b"#")
               self.comlink.flush()

if __name__ == '__main__':
        print("Testing LoadControl!")
        load = USBLoadControl(Config.LOAD_DEVICE)
        R = int(raw_input("Enter a resistance: "))
        L = int(raw_input("Enter a inductance: "))
        C = int(raw_input("Enter a capacatence: "))
        load.setRLC(int(R),int(L),int(C))
        time.sleep(5)
        load.reset()

