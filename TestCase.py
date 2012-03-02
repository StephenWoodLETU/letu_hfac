#provides a base class for the other testcases 

import sys
import time
class TestCase:
	def __init__(self, name):
		self.name=name
	def runtests(self):
		print "Would you like to run "+self.name+"?(Y/N)",
		respons=raw_input()
		if respons[0] != 'Y' and respons[0] != 'y':
			return False
		Started=time.time()
		ret=self.test()
		Finished=time.time()
		if ret:
			print self.name,"PASSED"
		else:
			print self.name,"FAILED"
		print "test took",Finished-Started,"seconds"
		return ret
	def test(self):
		print "Writing to screen"
		return True

if __name__ == '__main__':
	test=TestCase("FakeTest")
	test.runtests()

