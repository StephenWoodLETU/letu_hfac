#The Tune Power Test

from TestCase import TestCase
import Config
import Utils
import csv
import time
from LoadControl import LoadControl
from TuneControl import TunerControl
from FreqControl import FrequencyControl

class PowTest(TestCase):
        def __init__(self):
            TestCase.__init__(self, "Tune Power Test")
            self.tune = TunerControl(Config.TUNE_DEVICE)
            self.load = LoadControl(Config.LOAD_DEVICE)
            self.tran = FrequencyControl(Config.FREQ_DEVICE)
            
        def test(self):
        	"Test the transceiver at various frequency-load-power combinations"
		results = csv.writer(file(Config.PowerTestoutput,"wb"))
		frequencys=range(2,30) #in MHz for the moment
        	powerlevels=range(1,20)
		for frequency in frequencys:
			print("Setting to %g MHz" % frequency)
			self.tran.setFrequency(frequency*1000000)
			for powerlevel in powerlevels:
				if not self.prompt("Procede at power level %s?" % powerlevel):
					break
				print("Setting power: %g" % powerlevel)
				self.tran.setPower(powerlevel)
				for row in loadTable:
					# Set load
					self.load.setLCR(float(row[Config.D_L_COL]), float(row[Config.D_C_COL]), float(row[Config.D_R_COL]))
					print("Setting load: L: %g C: %g R: %g" %
					(float(row[Config.D_L_COL]), float(row[Config.D_C_COL]), float(row[Config.D_R_COL])))
				#test for correct tuning
				Started=time.time()
				self.tune.start()
				self.tune.waitForDone()
				Finished=time.time()
				#record results
				if self.tune.getFrequency() == self.freq.readFrequency():
					result= [frequency,Finished-Started,"Pass"]
				else:
					result= [frequency,Finished-Started,"Fail"]
				print result
				results.writerow(result)
		#set power back down
		self.tran.setPower(1)			

if __name__ == '__main__':
    t = PowTest()
    t.runtests()

