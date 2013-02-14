#The Tune Power Test

from TestCase import TestCase
import Config
import Utils
import csv
import time
from LoadControl import LoadControl
from TuneControl import TunerControl
from FreqControl import FrequencyControl

M2Hz = 1000000

class PowTest(TestCase):
        def __init__(self):
            TestCase.__init__(self, "Tune Power Test")
            self.load = LoadControl(Config.LOAD_DEVICE)
            self.tran = FrequencyControl(Config.FREQ_DEVICE)
            self.tune = TunerControl(Config.TUNE_DEVICE)
            
        def test(self):
                "Test the transceiver at various frequency-load combinations"
                results = csv.writer(file(Config.TuneTimeTestoutput,"wb"))
                results.writerow(["Frequency","Time","Status"])
                #load input data
                infile = file(Config.TABLE_J, "r")
                tableJ = [line for line in csv.reader(infile)][Config.J_HEADER_ROWS:]
                infile.close()
                for row in tableJ:
                  frequency = float(row[Config.J_FREQ_COL])
                  print("Setting to %g MHz" % frequency)
                  self.tran.setFrequency(frequency*M2Hz)
                  for offset in range(0,Config.J_LOADS_PER_VSR*Config.J_VSRS,3):
                      # Set load
                      self.load.setLCR(float(row[Config.J_L_COL+offset]),
                       float(row[Config.J_C_COL+offset]),
                       float(row[Config.J_R_COL+offset]))
                      print("Setting load: L: %g C: %g R: %g" %
                      (float(row[Config.J_L_COL+offset]),
                       float(row[Config.J_C_COL+offset]),
                       float(row[Config.J_R_COL+offset])))
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

if __name__ == '__main__':
    t = PowTest()
    t.runtests()

