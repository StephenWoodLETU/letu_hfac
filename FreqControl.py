# This controls the frequency of the transmitter, as well as the power.

class FrequencyControl:
	
	def __init__(self, device):
		"""Open a specific device as a frequency controller.  Device is
		a tuple with the first element being the com port on Windows or
		file name on Linux and the second element is the baud rate."""
		pass

	def __del__(self):
		pass

	def setFrequency(self, freq):
		pass

	def setPower(self, power):
		pass

	def start(self):
		pass
	
	def stop(self):
		pass

