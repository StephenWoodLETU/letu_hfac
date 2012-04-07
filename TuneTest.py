# The VSWR Tune Test

from TestCase import TestCase
import Config
import Utils
import csv
from LoadControl import LoadControl
from FreqControl import FrequencyControl

class TuneTest(TestCase):
    
    def __init__(self):
        TestCase.__init__(self, "VSWR Tune Test")
        self.loadSetter = LoadControl(Config.LOAD_DEVICE)
        self.freq = FrequencyControl(Config.FREQ_DEVICE)
    
    def test(self):
        currentVSWR = 0
        tableD = None # This is a 2 dimensional table of all the frequencies that will be tested in the procedure
        testResult = True
        
        # Load frequencies to test
        try:
            inFile = file(Config.TABLE_D, "r")
            tableD = [line for line in csv.reader(inFile)][Config.D_HEADER_ROWS:]
            inFile.close()
        except:
            print("Could not load frequencies to test (%s)" % Config.TABLE_D)
            return False
            
        #open output
        results = csv.writer(file(Config.TuneTestoutput,"wb"))
	results.writerow(["Frequency","Load (L, C, R)","VSWR","Status"])
		
        # Set current VSWR to first
        currentVSWR = float(tableD[0][Config.D_VSWR_COL])
        
        # Cycle through frequencies
        for line in tableD:
            curTestResult = False
            calcVSWR = 0
            roe = 0
            roeValues = None
            vswrFile = None
            
            # Set current VSWR to current test value, checking if different
            if(currentVSWR != float(line[Config.D_VSWR_COL]) and not self.prompt("Continue?")):
                return testResult
            currentVSWR = float(line[Config.D_VSWR_COL])
        
            #set freq?
            self.freq.setFrequency(float(line[Config.D_FREQ_COL]))
            # Set load
            self.loadSetter.setLCR(float(line[Config.D_L_COL]), float(line[Config.D_C_COL]), float(line[Config.D_R_COL]))
            print("Setting load: L: %g C: %g R: %g" %
                  (float(line[Config.D_L_COL]), float(line[Config.D_C_COL]), float(line[Config.D_R_COL])))
        
            # Prompt user to run the network analyzer and save to location
            while(vswrFile == None):
                print("Please set the network analyzer to  %s Hz" % line[Config.D_FREQ_COL])
                print("Please save the CSV data from the analyzer to %s" % Config.NET_RES_FILE)
                self.wait()
                try:
                    vswrFile = file(Config.NET_RES_FILE, "r")
                except:
                    print("Could not open input file")
        
            # Load the contents of the file
            roeValues = [newLine for newLine in csv.reader(vswrFile)][Config.NET_RES_HEADER_ROWS:]
            vswrFile.close()
        
            # Calculate average roe
            for roeLine in roeValues:
                roe += complex(str(roeLine[Config.NET_RES_ROE_COL]).replace("i", "j"))
            roe /= len(roeValues)
            
            # Calculate VSWR and compare to predicted
            calcVSWR = Utils.Vswr(roe)
            
            # Print results and set overall test to false if failed
            if(curTestResult):
                print("Pass for frequency %s" % (line[Config.D_FREQ_COL]))
                results.writerow([float(line[Config.D_FREQ_COL]),
                (line[Config.D_L_COL],line[Config.D_C_COL],line[Config.D_R_COL]),
                calcVSWR,"Pass"]) 
            else:
                print("Fail for frequency %s" % (line[Config.D_FREQ_COL]))
                results.writerow([float(line[Config.D_FREQ_COL]),
                (line[Config.D_L_COL],line[Config.D_C_COL],line[Config.D_R_COL]),
                calcVSWR,"Fail"])
                testResult = False
            
            
        return testResult
    
if __name__ == '__main__':
    t = TuneTest()
    t.runtests()
