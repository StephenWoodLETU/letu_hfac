# The controller for the actual tuner we are testing.

import serial

# Variables related to the communication protocol
START_MESSAGE = b"start;"
STOP_DELIMITER = ord(";")
CLEAR_CACHE_MESSAGE = b"clear;"

class TunerControl:
	
	def __init__(self, device):
		"""Open a specific device as the tuner to test.  Device is
		a tuple with the first element being the com port on Windows or
		file name on Linux and the second element is the baud rate."""
		
		try:
			self.device = serial.Serial(*device)
		except:
			print("Could not open device at %s with baud rate %d" % (device[0], device[1]))
			raise

	def __del__(self):
		self.device.close()

	def start(self):
		"""Tell the tuner to start the tuning process."""
		
		self.device.write(START_MESSAGE)
		self.device.flushOutput()

	def waitForDone(self):
		"""This waits for the tuner to send a specific character that
		means that it is finished tuning."""
		
		inByte = STOP_DELIM + 1
		while(inByte != STOP_DELIMETER):
			inByte = ord(self.device.read(1))
		

	def clearCache(self):
		"""Tell the tuner to clear the cache.  Do not tell the tuner to
		clear while it is tuning, the response is undefined."""
		
		self.device.write(STOP_MESSAGE)
		self.device.flushOutput()
if __name__ == '__main__':
	print("Testing TunerControl!")
	f = raw_input("Enter the device descriptor: ")
	b = int(raw_input("Enter the baud rate: "))
	cont = TunerControl((f, b))
	
	print("Clearing device cache...")
	cont.clearCache()
	
	print("Starting device...")
	cont.start()
	print("Started.  Waiting for done character...")
	cont.waitForDone()
	print("Done.")
	