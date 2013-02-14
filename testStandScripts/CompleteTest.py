# A test case that will test the VSWR and time to tune for
# each load combination, power, and frequency

#from IcomControl import IcomControl
from I2cLoadControl import I2cLoadControl
from USBLoadControl import USBLoadControl
from FakeLoadControl import FakeLoadControl
import datetime
import Config
import csv
import sys

def runTest() :
    #icomControl = IcomControl(config.ICOM_DEVICE)
    if Config.LOAD_IFACE == 'usb' :
        loadControl = USBLoadControl()
    elif Config.LOAD_IFACE == 'i2c' :
        loadControl = I2cLoadControl()
    else :
        loadControl = FakeLoadControl()
        
    # Prepare the csv output file
    timeNow = datetime.datetime.now();
    filename = 'output/testResults' + timeNow.isoformat('_').replace(':', '.') + '.csv'
    if sys.version_info >= (3,0,0):
        outFile = open(filename, 'w', newline='')
    else:
        outFile = open(filename, 'wb')
    csvResults = csv.writer(outFile)
    csvResults.writerow(['RLC', 'Frequency', 'Power', 'Time Test Result', 'Time To Tune', 'VSWR Test Result', 'Measured VSWR'])

    # Copy some values from the config file
    attendedTest = Config.ATTENDED_TEST


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
        if attendedTest : print('Telling the load Arduino to set load: ', rlcCombo)
        loadControl.setRLC(rlcCombo[0], rlcCombo[1], rlcCombo[2])
        
        for freq in freqsToTest :
            # tell icom to set frequency
            if attendedTest : print('Telling the Icom to set frequency: ', freq)
            
            for power in powersToTest :
                # tell icom to set power
                if attendedTest : print('Telling the Icom to set power: ', power)
                
                if Config.COMPETITOR_TUNER :
                    # Tell the icom to tune
                    if attendedTest : print('Telling the Icom to start tuning.')
                    # Call wait for VSWR function
                else :
                    # Tell the HFAC arduino to tune
                    if attendedTest : print('Telling the HFAC Arduino to start tuning.')
                    # Wait for signal back
                    
                if attendedTest : print('Recording the test results.')
                csvResults.writerow([rlcCombo, freq, power])
    return True

if __name__ == '__main__':
    runTest()