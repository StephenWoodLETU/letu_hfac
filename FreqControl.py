# This controls the frequency of the transmitter, as well as the power.

import time
import serial

class FrequencyControl:
	
	def __init__(self, device):
		"""Open a specific device as a frequency controller.  Device is
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

	def sendCommand(self, command, subcommand=b'', data=b''):
		line=b""
		
		# Create the output message
		line=line + chr(0xFE) + chr(0xFE) + chr(0x76) + chr(0xE0)
		
		line=line + command
		line=line + subcommand
		line=line + data
		
		line=line + chr(0xFD)
		
		self.comlink.write(line)
		self.comlink.flush()
		
	def readResponse(self, responseDataLen):
		# Check for the OK back
		#recvd = self.comlink.read(7)
		pass
		
	def setFrequency(self, freq):
		#self.sendCommand(0x05,0x00,b"")
		pass

	def setPower(self, power):
		pass

	def start(self):
		pass
	
	def stop(self):
		pass

if __name__ == '__main__':
	print("Testing FrequencyControl!")
	f = raw_input("Enter the device descriptor: ")
	b = int(raw_input("Enter the baud rate: "))
	cont = FrequencyControl((f, b))
	
	cont.sendCommand(chr(0x19),chr(0x00))
	cont.sendCommand(chr(0x03))
	cont.sendCommand(chr(0x03))
	cont.sendCommand(chr(0x03))
	#cont.sendCommand(chr(0x13),chr(0x00))
	#cont.sendCommand(0x0E,0x02)
	#cont.sendCommand(0x0E,0x00)

