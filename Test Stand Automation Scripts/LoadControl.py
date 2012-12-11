# This file communicates with the load Arduino over I2C

import time
import smbus

# The default address for the arduino to be found at
DEFAULT_ADDRESS = 0x10

# The bounds for the resistance, inductance, and capacitance
R_BOUNDS = (2, 1000)
L_BOUNDS = (31, 8000)
C_BOUNDS = (15, 18800)

def _clamp(value, bounds):
        """Return value within the boundaries given.  Bounds is a tuple with the
        lower and upper limits."""
        
        return min(max(value, bounds[0]), bounds[1])

class LoadControl:
        
        def __init__(self, arduinoAddress = DEFAULT_ADDRESS):
                """Connect to an Arduino on a specific I2C address specified by
                address.  This throws an exception if it cannot use I2C."""
                
                try:
                    self.smbus = smbus.SMBus(0)
                    self.address = arduinoAddress
                except IOError:
                    print "Could not open connection to load control arduino!"
                    raise
        
        def setLoad(self, l, c, r):
                """Set the load (inductance, capacitance, and resistance in that
                order) and return the combined amount that could not be met.
                The returned value is probably not very useful unless you are
                checking that each load was met exactly, in which case it will
                be 0."""
                
                totalRemainder = 0
                
                totalRemainder += self.setInductance(l)
                totalRemainder += self.setCapacitance(c)
                totalRemainder += self.setResistance(r)
                
                return totalRemainder
               
        def _getRemainder(self):
                """Get the remainder of the capacitance, inductance, or
                resistance that could not be fulfilled in the last command or -1
                if there was an error reading from the device."""
                
                try:
                        return self.smbus.read_byte(self.address)
                except:
                        return -1
               
        def _sendCommand(self, command, data):
                """Send a low-level command to the device along with an integer
                argument."""
                
                try:
                        command = map(ord, str(command))
                        argument = map(ord, str(data))
                        for byte in command + argument + [0]:
                                self.smbus.write_byte(self.address, byte)
                except IOError:
                        return -1
               
        def setResistance(self, r):
                """Set the resistance (ohms) of the load and return the amount
                that could not be met or -1 if the connection was lost."""
                
                self._sendCommand("SETR", _clamp(int(r), R_BOUNDS))
                return self._getRemainder()
                
        def setInductance(self, l):
                """Set the inductance (mH) of the load and return the amount
                that could not be met or -1 if the connection was lost."""
                
                self._sendCommand("SETL", _clamp(int(l), L_BOUNDS))
                return self._getRemainder()
                
        def setCapacitance(self, c):
                """Set the capacitance (uF) of the load and return the amount
                that could not be met or -1 if the connection was lost."""
                
                self._sendCommand("SETC", _clamp(int(c), C_BOUNDS))
                return self._getRemainder()

if __name__ == '__main__':
        print("Testing LoadControl!")
        load = LoadControl()
        L = int(raw_input("Enter a load: "))
        C = int(raw_input("Enter a capacatence: "))
        R = int(raw_input("Enter a resistance: "))
        load.setLoad(L,C,R)
        
