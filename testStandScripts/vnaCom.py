from scpi import SCPI
import serial

class vnaCom():
        
        def __init__(self, device, ip):
            try:
                self.device = device
                self.comlink = serial.Serial(*device)
            except:
                 print("Could not open ",device)
                 raise
            self.scpi = SCPI(ip)

        
        def __del__(self):
               self.comlink.close()

        def sendMagAndPhase(self):
            (mag,phase) = self.scpi.getMagAndPhase()

            # Format is mag,phase (floats);
            command = b"{0},{1}\n".format(mag, phase)
            self.comlink.write(command)

            self.comlink.flush()
            return (mag,phase)

        def waitForRequest(self):
            response = self.comlink.readline()

            while response.find('GETMAGPHASE') != 0 :
                response = self.comlink.readline()
                print response


if __name__ == '__main__':
    dev = "/home/pi/serial/ttyARD2"
    baud = 9600
    print "Using device: " + dev
    print "Using baud rate: {0}".format(baud)
    ip = "10.52.88.137"
    print "Using IP: " + ip
    com = vnaCom((dev,baud),ip)

    while True :
        print "Waiting for a request from the Arduino"
        com.waitForRequest()
        print "Request made. Sending magnitude and phase"
        (mag,phase) = com.sendMagAndPhase()
        print "Sent magnitude: {0} and phase: {1}".format(mag,phase)
