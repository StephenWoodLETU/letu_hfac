# Fake class for controlling the variable load

from LoadControl import LoadControl

class FakeLoadControl(LoadControl):
    
    def setRLC(self, r, l, c):
        """Set the RLC of the variable load"""
        print("FAKE_LOAD: Set RLC: {0} {1} {2}".format(r, l, c))
        return
        
    def reset(self):
        """Set the load to zero impedence"""
        print("FAKE_LOAD: Reset the load")
        return
        
if __name__ == '__main__':
    t = FakeLoadControl();
    t.reset();
