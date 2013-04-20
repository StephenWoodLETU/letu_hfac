import socket
import time
import struct

class SCPI:
    PORT = 5025

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        #self.f = self.s.makefile("rb")

        #RESET
        #self.s.send("*RST\n")
        #self.s.send("*CLS\n")

        #set output load
        #self.s.send("OUTPut:LOAD INF\n")

    def setScreen(self, isOn):
        self.s.send("DISP:ENABLE %d" % isOn)


    def getMeasurement(self):
        self.s.send("CALC:MARK1:Y?")
        meas = self.s.recv(5)
        return meas


if __name__ == '__main__':
    print("Testing SCPI control")

    #ip = raw_input("Enter the IP address: ")
    #onOff = int(raw_input("Screen on or off? [0 or 1]: "))
    ip = "10.52.88.163"
    scpi = SCPI(ip)
    #scpi.setScreen(onOff)
    meas = scpi.getMeasurement()
    print(meas)
    
