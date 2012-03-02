# The VSWR Tune Test

import TestCase
import Config
import Utils
import csv

class TuneTest(TestCase):
    
    def test(self):
        currentVSWR = 0
        tableD = None # This is a 2 dimensional table of all the frequencies that will be tested in the procedure
        testResult = True
        
        # Load frequencies to test
        try:
            inFile = file(Config.TABLE_D, "r")
            tableD = csv.reader(inFile)
            inFile.close()
        except:
            print("Could not load frequencies to test (%s)" % Config.TABLE_D)
            return False
        
        # Set current VSWR to first
        currentVSWR = float(tableD[1][Config.D_VSWR_COL])
        
        # Cycle through frequencies
        for line in tableD[1:]:
            curTestResult = False
            calcVSWR = 0
            roe = 0
            roeValues = None
            vswrFile = None
            
            # Set current VSWR to current test value, checking if different
            if(currentVSWR != line[Config.D_VSWR_COL] and not self.prompt("Continue (Y/N)")):
                return testResult
            currentVSWR = line[Config.D_VSWR_COL]
        
            # Set load
        
            # Prompt user to run the network analyzer and save to location
            while(vswrFile == None):
                print("Please save the CSV network analyzer output to %s" % Config.NET_RES_FILE)
                self.wait()
                try:
                    vswrFile = file(Config.NET_RES_FILE, "r")
                except:
                    print("Could not open input file")
        
            # Load the contents of the file
            roeValues = csv.reader(vswrFile)
            vswrFile.close()
        
            # Calculate average roe
            for roeLine in roeValues:
                roe += complex(str(roeLine[Config.NET_RES_ROE_COL]).replace("i", "j"))
            roe /= len(roeValues)
            
            # Calculate VSWR and compare to predicted
            calcVSWR = Utils.Vswr(roe)
            
            # Print pass fail
            if(not curTestResult):
                testResult = False
                
            if(curTestResult):
                print("Pass for frequency %s" % (tableD[Config.D_FREQ_COL]))
            else:
                print("Fail for frequency %s" % (tableD[Config.D_FREQ_COL]))
            
        return testResult
    
if __name__ == '__main__':
    t = TuneTest()
    t.runtests()