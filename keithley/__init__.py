import serial
import time
import csv


class keithley(object):

    i_lim = 0.001
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
        self.write(':SYST:BEEP:STATE OFF') # Turn off the beeping
        self.write(':ROUT:TERM FRON')      # Send voltage to front
        self.write(':SENS:FUNC:ON "CURR", "VOLT"')
        # self.write('SENS:FUNC:CONC 1')
        self.write(':FORM:ELEM VOLT, CURR, TIME')

        # for command in self.init_commands:
        #     self.ser.write(command)

        print 'Keithley on', self.ser.name, 'initialized.'

    def write(self, command):
        self.ser.write(command+'\n')

    def set_mode(self, mode='V'):
        if mode == 'V':
            self.write(':SOUR:FUNC:MODE VOLT')
            self.write(':SOUR:VOLT:MODE FIX')
        elif mode == 'I':
            self.write(':SOUR:FUNC:MODE CURR')
            self.write(':SOUR:CURR:MODE FIX')
        else:
            print "Expecting mode 'V' or 'I'."

    def read(self):
        self.write('READ?')
        data = self.ser.readline()
        try:
            data = map(float, data.split(','))
            data = [data[2], data[0], data[1]]
        except:
            pass
        return data

    def __del__(self):
        self.output('OFF')
        print 'Keithley on', self.ser.name, 'released.'
        self.ser.close()

    def capture(self, t=10, filename='data.csv'):
        t0 = time.time()
        dt = 0
        data=[]
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['T', 'V', 'I'])
            while dt < t:
                dt = time.time()-t0
                data.append(self.read())
                time.sleep(0.1)
                writer.writerow(data[-1])
        return data

    def set_term(self, loc='FRON'):
        self.write(':ROUT:TERM '+loc)

    def set_i_range(self, val):
        pass

    def output(self, mode='OFF'):
        if mode in ['ON', 'OFF']:
            self.write(':OUTP ' + mode)
        else:
            print "Expecting 'ON' or 'OFF'."

    def set_v(self, V=0):
        self.write(':SOUR:VOLT '+str(V))

    def set_i(self, I=0):
        self.write(':SOUR:CURR '+str(I))


if __name__ == '__main__':
    k = keithley('COM7')
    k.write(':SENS:CURR:RANG 1e-6')
    k.write(':SENS:CURR:RANG:AUTO 1')
    k.write(':SENS:CURR:PROT .001')
    k.write(':SENS:CURR:NPLC 1')
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


                    #  ':SOUR:VOLT '+str(V)
