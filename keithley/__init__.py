import serial
import time


class keithley(object):

    i_lim = 0.001
    V = 500
    init_commands = ['*RST',
                     ':ROUT:TERM FRON',
                     ':SENS:FUNC:CONC 1',
                     ':SENS:FUNC:ON "CURR", "VOLT"',
                     ':SENS:CURR:RANG 1e-6',
                     ':SENS:CURR:RANG:AUTO 1',
                     ':SENS:CURR:PROT ' + str(i_lim),
                     ':SENS:CURR:NPLC 1',
                     ':SENS:AVER:STAT 0',
                     ':SOUR:CLE:AUTO OFF',
                     ':SOUR:FUNC:MODE VOLT',
                     ':SOUR:VOLT:MODE FIX',
                     ':SOUR:VOLT:RANG 500.0',
                     ':SOUR:VOLT:RANG:AUTO 1',
                     ':SOUR:VOLT '+str(V)]

    def __init__(self, port=0):
        self.ser = serial.Serial(port, )
        self.write = self.ser.write
        for command in init_commands:
            self.write(command)
        print ser.name, 'initialized.'

    def __del__(self):
        self.write(':OUTP OFF')
        self.ser.close()

    def _capture(self, t=10, filename='data.csv'):
        t0 = time.time()
        dt = 0
        V_list = []
        t_list = []
        while dt < t:
            dt = time.time()-t0
            self.write('READ?')
            V_list.append = float(self.readline())
            t_list.append(dt)
            wait(0.1)
        return (t_list, V_list)

    def capture(filename):
        pass

    def set_term(self, loc='FRON'):
        self.write(':ROUT:TERM '+loc)

    def set_i_range(self, val):
        pass

if __name__ == '__main__':
    a = keithley()
