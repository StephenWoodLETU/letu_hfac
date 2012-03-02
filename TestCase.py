#provides a base class for the other testcases 

import sys
import time
class TestCase:
	"A base class for building test, provides some usful functions"
	def __init__(self, name):
		self.name=name

	def runtests(self):
		"Call this to actually run the test"
		self.prompt("Would you like to run "+self.name+"?(Y/N)")
		Started=time.time()
		ret=self.test()
		Finished=time.time()
		if ret:
			print self.name,"PASSED"
		else:
			print self.name,"FAILED"
		print "test took",Finished-Started,"seconds"
		return ret

	def prompt(self, text):
		"Promts the user for a yes/no answer"
		print text,
		while True:
			response=raw_input()
			if response[0] == 'Y' or response[0] == 'y':
				return True
			if response[0] == 'N' or response[0] == 'n':
				return False
			print "Please enter Y or N",
	def wait(self):
		"Waits for the user to push [enter]"
		print "Push [enter] to continue",
		raw_input()
		
	def test(self):
		"Override this with the aproprate test actions"
		print "Writing to screen"
		print "Waiting for user to finnish"
		self.wait()
		return True

if __name__ == '__main__':
	test=TestCase("FakeTest")
	test.runtests()

