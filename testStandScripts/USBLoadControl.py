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
               command = b"{0},{1},{2}".format(r, l, c)
               self.comlink.write(command)
               # Wait until the arduino is done setting the load
               self.comlink.readline()
               self.comlink.flush()
               

        def reset(self):
               # 
               self.comlink.write("0,0,0")
               self.comlink.flush()

if __name__ == '__main__':
        print("Testing LoadControl!")
        load = USBLoadControl(Config.LOAD_DEVICE)
        time.sleep(1)
        #R = int(raw_input("Enter a resistance: "))
        #L = int(raw_input("Enter a inductance: "))
        #C = int(raw_input("Enter a capacatence: "))
        R = 1000
        L = 0
        C = 0
        load.setRLC(R, L, C)
        print("Done setting the load.")
        raw_input("Ready to reset? [Enter]")

