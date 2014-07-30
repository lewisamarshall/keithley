if __name__ == '__main__':
    import sys
    sys.path.append('/usr/local/lib/python2.7/site-packages')

import serial
import time
import csv
import sys


class keithley(object):

    i_lim = 0.01
    V = 500
    init_commands = ['*RST',
                     ':ROUT:TERM FRON',
                     ':SENS:FUNC:CONC 1',
                     ':SENS:CURR:RANG 1e-6',
                     ':SENS:CURR:RANG:AUTO 1',
                     ':SENS:CURR:PROT ' + str(i_lim),
                     ':SENS:CURR:NPLC 1',
                     ':SENS:AVER:STAT 0',
                     ':SOUR:CLE:AUTO OFF',
                     ':SOUR:VOLT:RANG 500.0',
                     ':SOUR:VOLT:RANG:AUTO 1',
                     ':SOUR:VOLT '+str(V)]

    def __init__(self, port=0):
        self.ser = serial.Serial(port, timeout=1)
        self.ser.flush()
        self.write('*cls')
        self.write('*rst')
        self.write('*idn?')
        self.identity = self.ser.readline()
        print self.identity
        self.write(':SYST:BEEP:STATE OFF')  # Turn off the beeping
        # self.write(':ROUT:TERM FRON')      # Send voltage to front
        # self.write(':SENS:FUNC:ON "CURR", "VOLT"')
        # self.write('SENS:FUNC:CONC 1')
        self.write(':FORM:ELEM VOLT, CURR, TIME')

        # for command in self.init_commands:
        #     self.ser.write(command)

        print 'Keithley on', self.ser.name, 'initialized.'

    def write(self, command):
        if sys.platform == 'win32':
            self.ser.write(command+'\n')
        elif sys.platform == 'darwin':
            self.ser.write(command+'\n')
        else:
            self.ser.write(command+'\n')

    def set_mode(self, mode='V'):
        if mode == 'V':
            self.write(':SOUR:FUNC:MODE VOLT')
            self.write(':SOUR:VOLT:MODE FIX')
        elif mode == 'I':
            self.write(':SOUR:FUNC:MODE VOLT')
            self.write(':SOUR:VOLT:MODE FIX')
        else:
            print "Expecting mode 'V' or 'I'."

    def read(self):
        self.write('READ?')
        data = self.ser.readline()
        try:
            data = map(float, data.lstrip().rstrip().split(','))
            data = [data[2], data[0], data[1]]
        except:
            pass
        return data

    def __del__(self):
        # self.output('OFF')
        print 'Keithley on', self.ser.name, 'released.'
        self.ser.close()

    def capture(self, t=10, filename='data.csv', mode='wb'):
        t0 = time.time()
        dt = 0
        data=[]
        with open(filename, mode) as file:
            writer = csv.writer(file)
            if 'w' in mode:
                writer.writerow(['T', 'V', 'I'])
            while dt < t:
                dt = time.time()-t0
                data.append(self.read())
                time.sleep(0.1)
                if data[-1]:
                    writer.writerow(data[-1])
        return data

    def set_term(self, loc='FRON'):
        self.write(':ROUT:TERM '+loc)

    def set_i_range(self, val):
        pass

    def output(self, mode='OFF'):
        if mode in ['ON', 'OFF']:
            self.write(':OUTPUT ' + mode)
        else:
            print "Expecting 'ON' or 'OFF'."

    def set_v(self, V=0):
        self.write(':SOUR:VOLT '+str(V))

    def set_i(self, I=0):
        self.write(':SOUR:CURR '+str(I))

    def close(self):
        self.__del__



if __name__ == '__main__':
    print sys.platform
    if sys.platform == 'darwin':
        k = keithley('/dev/tty.PL2303-00001014')
    elif sys.platform == 'win32':
        k = keithley('COM7')
    k.write(':SENS:CURR:RANG 1e-6')
    k.write(':SENS:CURR:RANG:AUTO 1')
    k.write(':SENS:CURR:PROT .001')
    k.write(':SENS:CURR:NPLC 2')
    k.write(':SENS:AVER:STAT 0')
    k.write(':SOUR:CLE:AUTO OFF')
    k.write(':SOUR:VOLT:RANG 500.0')
    k.write(':SOUR:VOLT:RANG:AUTO 1')
    k.set_v(100)
    # k.set_mode('I')
    # k.set_i(.001)
    k.output('ON')
    k.capture()
    k.output('OFF')
    del k
