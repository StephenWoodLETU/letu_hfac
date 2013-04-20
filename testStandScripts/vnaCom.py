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
            (mag,phase) = scpi.getMagAndPhase()

            # Format is mag,phase (floats);
            command = b"{0},{1}".format(mag, phase)
            self.comlink.write(command)

            self.comlink.flush()
            return (mag,phase)

        def waitForRequest()
            response = ''

            while response != 'GETMAGPHASE' :
                response = self.comlink.readline()


if __name__ == '__main__':
    dev = raw_input("Enter the Arduino device to connect to: ")
    baud = raw_input("Enter the baud rate of the Arduino: ")
    ip = raw_input("Enter the VNA IP address: ")
    com = vnaCom((dev,baud),ip)

    while True :
        print "Waiting for a request from the Arduino"
        com.waitForRequest()
        print "Request made. Sending magnitude and phase"
        (mag,phase) = com.sendMagAndPhase()
        print "Sent magnitude: {0} and phase: {1}".format(mag,phase)
