# This file communicates with the load Arduino.
# The format for this is:
#  setup by sending "L C R;"
#  reset by sending "<char>"

import serial 

class LoadControl:
	
	def __init__(self, device):
		"""Open a specific device as a load controller.  Device is
		a tuple with the first element being the com port on Windows or
		file name on Linux and the second element is the baud rate."""
		try:
			self.device = device
			self.comlink = serial.Serial(*device)
		except:
			print "Could not open ",device
			raise
	
	def __del__(self):
		self.comlink.close()

	def setLCR(self, l, c, r):
		# Format is L C R;
		command = b"{0} {1} {2};".format(l,c,r)
		self.comlink.write(command)
		self.comlink.flush()

	def reset(self):
		# Format is <char>
		self.comlink.write(b"#")
		self.comlink.flush()
