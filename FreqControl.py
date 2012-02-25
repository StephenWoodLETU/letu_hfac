# This controls the frequency of the transmitter, as well as the power.

import time
import serial

# Utilities for converting BCD to decimal and back
def _BCD_To_Int(bcdStr):
	"""Convert a binary coded decimal to an integer."""
	val = 0
	multiplier = 1
	
	for curChar in bcdStr[::-1]:
		
		# Decode first digit
		curVal = ord(curChar) & 0x0F
		val = val + multiplier * curVal
		multiplier *= 10
		
		# Add second digit
		curVal = ord(curChar) >> 4
		val = val + multiplier * curVal
		multiplier *= 10
		
	return val

def _Int_To_BCD(num):
	"""Convert an integer to a binary coded decimal to a string."""
	val = int(num)
	toRet = b""
	
	while(val > 0):
		
		# Encode first digit
		curChar = (val % 10)
		val = val / 10
		
		# See if we have another digit to encode
		if(val > 0):
			curChar = curChar | ((val % 10) << 4)
			val = val / 10
			
		# Append
		toRet = chr(curChar) + toRet
		
	return toRet

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

	def _sendCommand(self, command, subcommand=b'', data=b''):
		line=b""
		
		# Create the output message
		line=line + chr(0xFE) + chr(0xFE) + chr(0x76) + chr(0xE0)
		
		line=line + command
		line=line + subcommand
		line=line + data
		
		line=line + chr(0xFD)
		
		self.comlink.write(line)
		self.comlink.flush()
		
	def _readResponse(self, responseDataLen):
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
	
	cont._sendCommand(chr(0x19),chr(0x00))
	cont._sendCommand(chr(0x03))
	cont._sendCommand(chr(0x03))
	cont._sendCommand(chr(0x03))
	#cont._sendCommand(chr(0x13),chr(0x00))
	#cont._sendCommand(0x0E,0x02)
	#cont._sendCommand(0x0E,0x00)

