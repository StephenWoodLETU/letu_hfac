# This controls the PowerMasterII for detecting VSWR

class PMControl:
    def __init__(self, device):
        ""Open a device (linux file) to communicate with to control
        the PowerMaster (PM)""
        try:
            # Open device here
            
        except:
            print "Could not open ", device
            raise
            
    # def __del__(self):
    
    def getVSWR(self):
        # get the VSWR from the PM
        
        return 1
        
    def 