# This runs the infamous "Power Test"

from TestCase import TestCase
import Config
import csv
from FreqControl import FrequencyControl

class PowerTest(TestCase):
    
    def __init__(self):
        TestCase.__init__(self, "Power Test")
        self.freqSetter = FrequencyControl(Config.FREQ_DEVICE)
    
    def test(self):
        tableF = None # This is a 2 dimensional table of all the combinations of loads and frequenices to be tested
        testResult = True
        powers = None;
        frequencies = None;

        #open output        
        results = csv.writer(file(Config.PowerTestoutput,"wb"))
        results.writerow(["Powerlevel","Frequency","Heat","Correctness"])

        # Load frequencies to test
        try:
            inFile = file(Config.TABLE_F, "r")
            tableF = [line for line in csv.reader(inFile)][Config.F_HEADER_ROWS:]
            inFile.close()
        except:
            print("Could not load frequencies to test (%s)" % Config.TABLE_F)
            return False
        
        # Load all powers and frequencies from the table
        powers = [line[Config.F_ALL_POWERS_COL] for line in tableF if line[Config.F_ALL_POWERS_COL] != ""]
        frequencies = [line[Config.F_ALL_FREQS_COL] for line in tableF if line[Config.F_ALL_FREQS_COL] != ""]
        
        # Cycle through powers
        for power in powers:
            curPower = float(power)
            
            # Set power - MAY NEED CONVERSION
            self.freqSetter.setPower(curPower)
            
            for freq in frequencies:
                curFreq = float(freq) * 1000000
                curTestResult = True
                print("Running test for power %f W and %f MHz" %(curPower, curFreq / 1000000))
                
                # Set frequency
                self.freqSetter.setFrequency(curFreq)
                
                # Ask user if everything is OK
                if(not self.prompt("Is the equipment cool enough?")):
                     self.freqSetter.setPower(0)
                     results.writerow([curPower,curFreq,"Overheated!","Failed"])
                     return False
                    
                # Prompt for if the test is good
                curTestResult = self.prompt("Is the output correct?")
                
               #save what just happend
               results.writerow([curPower,curFreq,"Pass",curTestResult])
                # Print results and set overall test to false if failed
                if(curTestResult):
                    print("PASS for power %f W frequency %s MHz\n" % (curPower, curFreq / 1000000))
                else:
                    print("FAIL for power %f W frequency %s MHz\n" % (curPower, curFreq / 1000000))
                    testResult = False
            
        return testResult
    
if __name__ == '__main__':
    t = PowerTest()
    t.runtests()
