# The controller for the actual tuner we are testing.

class TunerControl:
	
	def __init__(self, device):
		"""Open a specific device as the tuner to test.  Device is
		a tuple with the first element being the com port on Windows or
		file name on Linux and the second element is the baud rate."""
		pass

	def __del__(self):
		pass

	def start(self):
		pass

	def waitForDone(self):
		pass

	def clearCache(self):
		pass

