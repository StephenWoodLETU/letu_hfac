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
            inFile = file(Config.TABLE_J, "r")
            tableJ = [line for line in csv.reader(inFile)][Config.J_HEADER_ROWS:]
            inFile.close()
        except:
            print("Could not load frequencies to test (%s)" % Config.TABLE_J)
            return False
            
        #open output
        results = csv.writer(file(Config.TuneTestoutput,"wb"))
	results.writerow(["Frequency","Load (L, C, R)","VSWR","Status","Visual"])
		
        # Set current VSWR to first
        for currentVSWR in [2, 3, 5, 10, 20]:
        
		# Cycle through frequencies
		for line in tableJ:
		    curTestResult = False
		    calcVSWR = 0
		    roe = 0
		    roeValues = None
		    vswrFile = None
		    		
		    #set freq?
		    self.freq.setFrequency(float(line[Config.J_FREQ_COL]))
		    for offset in range(0,Config.J_LOADS_PER_VSR*Config.J_VSRS,3):
			    # Set load
                            print("Items %s %s %s" %
				  (line[Config.J_L_COL+offset],
		                   line[Config.J_C_COL+offset],
		                   line[Config.J_R_COL+offset]))
			    print("Setting load: L: %g C: %g R: %g" %
				  (float(line[Config.J_L_COL+offset]),
		                   float(line[Config.J_C_COL+offset]),
		                   float(line[Config.J_R_COL+offset])))
			    self.loadSetter.setLCR(
				float(line[Config.J_L_COL+offset]),
				float(line[Config.J_C_COL+offset]),
				float(line[Config.J_R_COL+offset]))
		
			    # Prompt user to run the network analyzer and save to location
			    while(vswrFile == None):
				    print("Please set the network analyzer to  %s Hz"
					 % line[Config.J_FREQ_COL])
				    print("Please save the CSV data from the analyzer to %s"
					 % Config.NET_RES_FILE)
				    self.wait()
				    try:
					vswrFile = file(Config.NET_RES_FILE, "r")
				    except:
					print("Could not open input file") 
			    print "Does the graph look correct? :",
			    notes = raw_input()
			    
			    # Load the contents of the file
			    roeValues = [newLine for newLine in csv.reader(vswrFile)][Config.NET_RES_HEADER_ROWS:]
			    vswrFile.close()

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
			    
			    # Print results and set overall test to false if failed
			    if(curTestResult):
				print("Pass for frequency %s" % (line[Config.J_FREQ_COL]))
				results.writerow([float(line[Config.J_FREQ_COL]),
				(line[Config.J_L_COL],line[Config.J_C_COL],line[Config.J_R_COL]),
				calcVSWR,"Pass",notes]) 
				testResult = True
			    else:
				print("Fail for frequency %s" % (line[Config.J_FREQ_COL]))
				results.writerow([float(line[Config.J_FREQ_COL]),
				(line[Config.J_L_COL],line[Config.J_C_COL],line[Config.J_R_COL]),
				calcVSWR,"Fail",notes])
				testResult = False    
            	if(not self.prompt("Continue?")):
		        return testResult
        return testResult
    
if __name__ == '__main__':
    t = TuneTest()
    t.runtests()
