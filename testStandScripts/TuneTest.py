# The VSWR Tune Test

from TestCase import TestCase
import Config
import Utils
import csv
from LoadControl import LoadControl
from FreqControl import FrequencyControl

MHz = 1000000

class TuneTest(TestCase):
    
    def __init__(self):
        TestCase.__init__(self, "VSWR Tune Test")
        #moved this into the test
        #self.loadSetter = LoadControl(Config.LOAD_DEVICE)
        self.freq = FrequencyControl(Config.FREQ_DEVICE)
    
    def test(self):
        currentVSWR = 0
        tableD = None # This is a 2 dimensional table of all the frequencies that will be tested in the procedure
        testResult = True
        # Load frequencies to test
        try:
            inFile = file(Config.TABLE_J, "r")
            tableJ = [line for line in csv.reader(inFile)][Config.J_HEADER_ROWS:]
            inFile.close()
        except:
            print("Could not load frequencies to test (%s)" % Config.TABLE_J)
            return False
            
        #open output
        results = csv.writer(file(Config.TuneTestoutput,"wb"))
        results.writerow(["Frequency [MHz]","Inductor","Capacitor","Resistor","Final VSWR","Status","Raido SWR meter value:"])
        
        # Cycle through frequencies
        for line in tableJ:
            curTestResult = False
            calcVSWR = 0
            roe = 0
            roeValues = None
            vswrFile = None
            
            frequency = float(line[Config.J_FREQ_COL])
            #set freq
            self.freq.setFrequency(frequency*MHz)
            self.loadSetter = LoadControl(Config.LOAD_DEVICE)
            for offset in range(0,Config.J_LOADS_PER_VSR*Config.J_VSRS,3):        
                # Set load
                L = float(line[Config.J_L_COL+offset])
                C = float(line[Config.J_C_COL+offset])
                R = float(line[Config.J_R_COL+offset])
                print("Setting load: L: %g C: %g R: %g" % (L,C,R))
                self.loadSetter.setLCR(L,C,R)
                              
                # Prompt user to run the network analyzer and save to location
                while(vswrFile == None):                    
                    print("Please wait until tuned")
                    print("Input raido SWR meter value:"),
                    notes = raw_input()
                    print("Press enter to set raio to recieve")
                    self.wait()
                    self.freq.setRx()
                    print("Please set the network analyzer to  %s MHz"
                     % line[Config.J_FREQ_COL])
                    print("Please save the CSV data from the analyzer to %s"
                     % Config.NET_RES_FILE)
                    self.wait()
                    try:
                        vswrFile = file(Config.NET_RES_FILE, "r")
                    except:
                        print("Could not open input file") 
                print("Reconnect the coupler to the transmitter then press enter")
                self.wait()
                self.freq.setTx()

                # Load the contents of the file
                roeValues = [newLine for newLine in csv.reader(vswrFile)][Config.NET_RES_HEADER_ROWS:]
                vswrFile.close()
                vswrFile = None
                # Calculate average roe 
                roeValues.pop()
                for roeLine in roeValues:
                    try:
                        roe += Utils.tooComplex(roeLine[Config.NET_RES_ROE_COL])
                    except IndexError:
                        print "Wiered input:",roeLine
                roe /= len(roeValues)
            
                # Calculate VSWR and compare to predicted
                calcVSWR = Utils.Vswr(roe)
                curTestResult = True if calcVSWR < 1.6 else False
                
                # Print results and set overall test to false if failed
                if(curTestResult):
                    print("Pass for frequency %s" % (frequency))
                    results.writerow([float(line[Config.J_FREQ_COL]),L,C,R,
                    calcVSWR,"Pass",notes]) 
                    testResult = True
                else:
                    print("Fail for frequency %s" % (frequency))
                    results.writerow([float(line[Config.J_FREQ_COL]),L,C,R,
                    calcVSWR,"Fail",notes])
                    testResult = False
            del self.loadSetter
            if(not self.prompt("Continue?")):
                return testResult
                
        #return testResult
    
if __name__ == '__main__':
    t = TuneTest()
    t.runtests()
