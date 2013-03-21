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
               self.comlink.flush()
               self.comlink.flushInput()
               command = b"{0},{1},{2}".format(r, l, c)
               self.comlink.write(command)
               # Wait until the arduino is done setting the load
               print self.comlink.readline()

        def reset(self):
               # 
               self.comlink.write("0,0,0")
               self.comlink.flush()

if __name__ == '__main__':
        print("Testing LoadControl!")
        load = USBLoadControl(Config.LOAD_DEVICE)
        R = int(raw_input("Enter a resistance: "))
        L = int(raw_input("Enter a inductance: "))
        C = int(raw_input("Enter a capacatence: "))
        load.setRLC(1000, 0, 0)
        #load.setRLC(500,0,0)
        print("Set the load now sleeping...")
        time.sleep(5)
        print("Done Sleeping.")

