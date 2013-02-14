# Class for controlling the variable load via I2C

from LoadControl import LoadControl

class I2cLoadControl(LoadControl):
       
    def setRLC(self, r, l, c):
        """Set the RLC of the variable load"""
        print("I2C_LOAD_STUB: Set RLC:", r, l, c)
        return
        
    def reset(self):
        """Set the load to zero impedence"""
        print("I2C_LOAD_STUB: Reset the load", r, l, c)
        return