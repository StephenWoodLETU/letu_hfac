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

	def sendBytes(self, command, subcommand, data=b''):
		line=b""
		line=line + chr(0xFE)
		line=line + chr(0xFE)
		line=line + chr(0x76)
		line=line + chr(command)
		line=line + chr(subcommand)
#		line=line + chr(data)
		line=line + chr(0xFD)
		self.comlink.write(line)
		self.comlink.flush()
	def setFrequency(self, freq):
		self.sendBytes(0x05,0x00,b"")

	def setPower(self, power):
		pass

	def start(self):
		pass
	
	def stop(self):
		pass

if __name__ == '__main__':
	print("Testing TunerControl!")
	f = raw_input("Enter the device descriptor: ")
	b = int(raw_input("Enter the baud rate: "))
	cont = FrequencyControl((f, b))
	cont.sendBytes(0x13,0x00)
	cont.sendBytes(0x0E,0x02)
	time.sleep(7)
	cont.sendBytes(0x0E,0x00)
	del cont

