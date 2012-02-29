# This controls the frequency of the transmitter, as well as the power.

import time
import serial

# Utilities for converting BCD to decimal and back
def _BCD_To_Int(bcdStr):
	"""Convert a binary coded decimal to an integer."""
	val = 0
	multiplier = 1
	
	for curChar in bcdStr:
		
		# Decode first digit
		curVal = ord(curChar) & 0x0F
		val = val + multiplier * curVal
		multiplier *= 10
		
		# Add second digit
		curVal = ord(curChar) >> 4
		val = val + multiplier * curVal
		multiplier *= 10
		
	return val

def _Int_To_BCD(num,pad=0):
	"""Convert an integer to a binary coded decimal to a string.  pad is the
	minimum length to make the string that will be returned."""
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
		toRet = toRet + chr(curChar)
	
	# Pad response to a certain number of bytes
	for i in range(len(toRet),pad):
		toRet = toRet + '\0'
		
	return toRet

class FrequencyControl:
	
	def __init__(self, device):
		"""Open a specific device as a frequency controller.  Device is
		a tuple with the first element being the com port on Windows or
		file name on Linux and the second element is the baud rate."""
		try:
			self.device = device
			self.comlink = serial.Serial(*device)
			
			# Send get ID
			self._sendCommand(chr(0x19),chr(0x00))
			self._readResponse(2)
			
		except:
			print "Could not open ",device
			raise

	def __del__(self):
		self.comlink.close()

	def _sendCommand(self, command, subcommand=b'', data=b''):
		"""Send a specific command to the device.  You must put the command,
		subcommand, and data into binary strings exactly how you want them
		sent."""
		line=b""
		
		# Create the output message
		line=line + chr(0xFE) + chr(0xFE) + chr(0x76) + chr(0xE0)
		
		line=line + command
		line=line + subcommand
		line=line + data
		
		line=line + chr(0xFD)
		
		self.comlink.write(line)
		self.comlink.flush()
		
		# Eat up the echoed command
		self.comlink.read(len(line))
		
	def _readResponse(self, responseDataLen):
		"""Read a certain number of bytes back from the frequency
		device.  This value must include the length of the command,
		subcommand, and data that you want to read, and the returned
		string will be all of these concatenated to each other."""
		recvd = self.comlink.read(4+responseDataLen+1)
		return recvd[5:5+responseDataLen]
		
	def setFrequency(self, freq):
		"Set the frequency, in hertz, of the device."
		self._sendCommand(chr(0x05), data=_Int_To_BCD(freq,pad=5))
		self._readResponse(1)
		
	def readFrequency(self):
		"Read the frequency, in hertz, of the device."
		self._sendCommand(chr(0x03))
		return _BCD_To_Int(self._readResponse(6)[1:6])

	def setPower(self, power):
		pass
		
	def getPower(self):
		pass

if __name__ == '__main__':
	print("Testing FrequencyControl!")
	f = raw_input("Enter the device descriptor: ")
	b = int(raw_input("Enter the baud rate: "))
	cont = FrequencyControl((f, b))
	
	print cont.readFrequency()
	cont.setFrequency(9300000)
	print cont.readFrequency()
