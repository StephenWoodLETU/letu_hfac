# A test case that will test the VSWR and time to tune for
# each load combination, power, and frequency

#from IcomControl import IcomControl
from I2cLoadControl import I2cLoadControl
from USBLoadControl import USBLoadControl
from FakeLoadControl import FakeLoadControl
#from PMControl import *
import datetime
import Config
import csv
import sys
from time import time 

def runTest() :
    
    if Config.LOAD_IFACE == 'usb' :
        loadControl = USBLoadControl()
    elif Config.LOAD_IFACE == 'i2c' :
        loadControl = I2cLoadControl()
    else :
        loadControl = FakeLoadControl()
    
    # Create the PM  and icom controller
    pmControl = PMControl(Config.PM_DEVICE)
    icomControl = IcomControl(config.ICOM_DEVICE)
    
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
        powersToTest = [line for line in csv.reader(inFile)][0]
        inFile.close()
    except:
        print("Could not load the frequency and power values to test from file %s!" % Config.POWER_AND_FREQ)
        return False
        
    for power in powersToTest :
        # tell icom to set power
        if attendedTest : print('Telling the Icom to set power: ', power)
        icomControl.setFrequency(power)
        
        for rlcCombo in varLoadCombos :
            # Tell Arduino to set load
            if attendedTest : print('Telling the load Arduino to set load: ', rlcCombo)
            loadControl.setRLC(rlcCombo[0], rlcCombo[1], rlcCombo[2])
            frequency = rlcCombo[3]
        
            # tell icom to set frequency
            if attendedTest : print('Telling the Icom to set frequency: ', frequency)
            icomControl.setFrequency(frequency)
            
            if Config.COMPETITOR_TUNER :
                # Tell the icom to tune
                if attendedTest : print('Setting Icom to Tx.')
                icomControl.setTx()
                timerStart = time()
                waitForVSWR(pmControl)
                tuneTime = time() - timerStart

            else :
                # Tell the HFAC arduino to tune
                if attendedTest : print('Telling the HFAC Arduino to start tuning.')
                timerStart = time()
                # Wait for signal back
                tuneTime = time() - timerStart
            
            vswr = pmControl.getVSWR()
            if tuneTime > Config.MAX_TUNE_TIME :
                timeTest = 'fail'
            else :
                timeTest = 'pass'
            
            if vswr > Config.MAX_VSWR :
                vswrTest = 'fail'
            else :
                vswrTest = 'pass'
                
            if attendedTest : print('Recording the test results.')
            csvResults.writerow([rlcCombo, frequency, power, timeTest, tuneTime, vswrTest, vswr])
            
            if attendedTest : 
                print('Test results: ')
                print('RLC\tFrequency\tPower\tTime Test Result\tTime To Tune\tVSWR Test Result\tMeasured VSWR')
                print('{} {} {}\t{}\t{}\t{}\t{}\t{}\t{}'.format(rlcCombo[0], rlcCombo[1], rlcCombo[2], frequency, power, timeTest, tuneTime, vswrTest, vswr))
                userResponse = input('Continue testing? [y/n]: ')
                while True :
                    if userResponse == 'y' :
                        break
                    elif userResponse == 'n' :
                        return True
                    else :
                        userResponse = input('What? Please enter y [to continue] or n [to stop]: ')
    return True

def waitForVSWR(pmControl) :
    vswr = 100
    
    while vswr > 3 and vswr != 0:
        vswr = pmControl.getVSWR()

    
if __name__ == '__main__':
    runTest()
