# A test case that will test the VSWR and time to tune for
# each load combination, power, and frequency

#from IcomControl import IcomControl
import Config
import csv

class CompleteTest:
    "A class to completely test an antenna coupler"
    
    def __init__(self):
        True
        #self.icomControl = IcomControl(config.ICOM_DEVICE)
        
    def test(self):
        testResult = True;
        
        # Read in RLC values for the variable load to switch in
        try:
            inFile = open(Config.VAR_LOAD_COMBOS, 'r')
            varLoadCombos = [line for line in csv.reader(inFile)][Config.VLC_HEADER_ROWS:]
            inFile.close()
        except:
            print("Could not load the RLC values for the variable load board from file %s!" % Config.VAR_LOAD_COMBOS)
            return False
            
        # Read in the powers (in Watts) and frequencies (in Hz) to tune at
        try:
            inFile = open(Config.POWER_AND_FREQ, 'r')
            powersToTest, freqsToTest = [line for line in csv.reader(inFile)]
            inFile.close()
        except:
            print("Could not load the frequency and power values to test from file %s!" % Config.POWER_AND_FREQ)
            return False
            
        for rlcCombo in varLoadCombos :
            # Tell Arduino to set load
            if Config.ATTENDED_TEST == True : print('Telling the load Arduino to set load: ', rlcCombo)
            
            for freq in freqsToTest :
                # tell icom to set frequency
                if Config.ATTENDED_TEST  == True : print('Telling the Icom to set frequency: ', freq)
                
                for power in powersToTest :
                    # tell icom to set power
                    if Config.ATTENDED_TEST == True : print('Telling the Icom to set power: ', power)
                    
                    if Config.COMPETITOR_TUNER :
                        # Tell the icom to tune
                        if Config.ATTENDED_TEST == True : print('Telling the Icom to start tuning.')
                        # Call wait for VSWR function
                    else :
                        # Tell the HFAC arduino to tune
                        if Config.ATTENDED_TEST == True : print('Telling the HFAC Arduino to start tuning.')
                        # Wait for signal back
                        
                    
            
        return testResult
        
if __name__ == '__main__':
    t = CompleteTest()
    t.test()