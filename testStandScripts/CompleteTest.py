# A test case that will test the VSWR and time to tune for
# each load combination, power, and frequency

from IcomControl import *
from I2cLoadControl import I2cLoadControl
from USBLoadControl import USBLoadControl
from FakeLoadControl import FakeLoadControl
from PMControl import *
import datetime
import Config
import csv
import sys
from time import time
import time

def runTest() :
    
    if Config.LOAD_IFACE == 'usb' :
        loadControl = USBLoadControl(Config.LOAD_DEVICE)
    elif Config.LOAD_IFACE == 'i2c' :
        loadControl = I2cLoadControl()
    else :
        loadControl = FakeLoadControl()
    
    # Create the PM  and icom controller
    pmControl = PMControl(Config.PM_DEVICE)
    icomControl = IcomControl(Config.ICOM_DEVICE)
    
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
        if attendedTest : print('Telling the Icom to set power: '+ str(power))
        raw_input('Continue? ')
        icomControl.setPower(int(power))

        for rlcCombo in varLoadCombos :
            # Tell Arduino to set load
            if attendedTest : print('Telling the load Arduino to set load: {0} {1} {2}'.format(rlcCombo[0], rlcCombo[1], rlcCombo[2]))
            raw_input("Continue? ")
            loadControl.setRLC(int(rlcCombo[0]), int(rlcCombo[1]), int(rlcCombo[2]))
            frequency = int(rlcCombo[3])
        
            # tell icom to set frequency
            if attendedTest : print('Telling the Icom to set frequency: ' + str(frequency))
            raw_input('Continue? ')
            icomControl.setFrequency(frequency)

            if Config.COMPETITOR_TUNER :
                # Tell the icom to tune
                if attendedTest : print('Setting Icom to Tx.')
                raw_input("Continue? ")
                icomControl.setTx()
                icomControl.startTune()
                timerStart = time.time()
                waitForVSWR(pmControl)
                tuneTime = time.time() - timerStart

            else :
                # Tell the HFAC arduino to tune
                if attendedTest : print('Telling the HFAC Arduino to start tuning.')
                timerStart = time.time()
                # Wait for signal back
                tuneTime = time.time() - timerStart
            
            vswr = pmControl.getVSWR()
            # stop transmitting power
            icomControl.setRx()

            if tuneTime > Config.MAX_TUNE_TIME :
                timeTest = 'fail'
            else :
                timeTest = 'pass'
            
            if (float(vswr) > Config.MAX_VSWR) or float(vswr) < 1:
                vswrTest = 'fail'
            else :
                vswrTest = 'pass'
                
            if attendedTest : print('Recording the test results.')
            csvResults.writerow([rlcCombo, frequency, power, timeTest, tuneTime, vswrTest, vswr])
            
            if attendedTest : 
                print('Test results: ')
                print('{0:15s} {1:10s} {2:6s} {3:10s} {4:10s} {5:8s} {6:7s}'.format('RLC', 'Frequency', 'Power', 'Time Test', 'Time', 'VSWR Test', 'Measured VSWR'))
                print('{0:4s} {1:4s} {2:4s} {3:10d} {4:6s} {5:10s} {6:10f} {7:8s} {8:7s}'.format(rlcCombo[0], rlcCombo[1], rlcCombo[2], frequency, power, timeTest, tuneTime, vswrTest, vswr))
                userResponse = raw_input('Continue testing? [y/n]: ')
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
    numOfGoodVswrs = 0

    timeoutStart = time.time()
    while (numOfGoodVswrs < 10) :
        vswr = pmControl.getVSWR()
        print('VSWR: ' + vswr)
        if (vswr < Config.MAX_VSWR && vswr > 1)
            numOfGoodVswrs = numOfGoodVswrs + 1
        if (time.time() - timeoutStart) > float(Config.MAX_TUNE_TIME) :
            break

    return
    
if __name__ == '__main__':
    runTest()
