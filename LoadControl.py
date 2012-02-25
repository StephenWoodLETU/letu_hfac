# This file communicates with the load Arduino.

class LoadControl:
	
	def __init__(self, device):
		"""Open a specific device as a load controller.  Device is
		a tuple with the first element being the com port on Windows or
		file name on Linux and the second element is the baud rate."""
		pass

	def __del__(self):
		pass

	def setLCR(self, l, c, r):

		# Format is 
		pass

	def reset(self):
		pass
