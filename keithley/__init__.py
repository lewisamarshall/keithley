import serial
import time


class keithley(object):

    def __init__(self, port=0):
        self.ser = serial.Serial(port, )
        print ser.name, 'initialized.'

    def __del__(self):
        self.ser.close()

    def capture(self):
        pass

    


if __name__ == '__main__':
    keithley()
