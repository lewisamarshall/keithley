if __name__ == '__main__':
    import sys
    sys.path.append('/usr/local/lib/python2.7/site-packages')

import serial
from serial.tools.list_ports import comports
import time
import csv
import sys
import threading
import warnings


class Keithley(object):

    i_lim = 0.01
    V = 500
    data ={'V':[], 'I':[], 't':[]}
    output_on = False
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

    def __init__(self, port=None, timeout=1):
        if port is None:
            print 'Automatically detecting COM ports.'
            ports = list(comports())
            print 'Detected %i ports.' % len(ports)
            port = ports[0][0]
            print 'Trying port ' + port + '.'
        # Set up threading access control.
        self.writable = threading.Lock()
        self.capturing = threading.Event()
        self.data_access = threading.Lock()
        self.plotting = threading.Event()

        # Acquire the serial port.
        self.ser = serial.Serial(port, timeout=timeout)

        # Flush the serial port and clear all errors from instrument.
        self.ser.flush()
        self.reset()

        # Identify the instrument.
        if not self.identify():
            warnings.warn('Not a Keithley 2410.')
            if self.identity is not None:
                print self.identity['make', 'model']
        else:
            print 'Keithley on', self.ser.name, 'initialized.'

        #Set up for operation.
        self.clear_errors()
        self.clear_buffer()
        self.beep('OFF')
        self.set_term('FRONT')
        # self.set_concurrent('ON')
        self.write(':SENS:AVER:STAT 0')
        # self.write(':SENS:FUNC:ON:ALL')
        self.write(':SENS:FUNC:ON "CURR", "VOLT"')
        self.write(':FORM:ELEM VOLT, CURR, TIME')

    def write(self, command):
        with self.writable:
            self.ser.write(command+'\n')

    def reset(self):
        self.write('*rst')

    def clear_errors(self):
        self.write('*cls')

    def clear_buffer(self):
        self.write(':TRAC:CLE')

    def set_concurrent(self, mode='ON'):
        self.write('SENS:FUNC:CONC ' + mode)

    def beep(self, state='OFF'):
        if state in ['ON', 'OFF']:
            self.write(':SYST:BEEP:STATE '+state)
        else:
            print "Expected 'ON' or 'OFF' as a state."

    def set_term(self, loc = 'FRONT'):
        self.write(':ROUT:TERM '+loc)

    def identify(self):
        self.write('*idn?')
        idn_str = self.ser.readline()
        if not idn_str:
            warnings.warn('No identification response.')
            self.identity = None
            return None
        else:
            idn_str = idn_str.split(',')
        self.identity = {'make':idn_str[0],
                    'model':idn_str[1],
                    'serial':idn_str[2],
                    'date':idn_str[3]}
        if self.identity['make'].startswith('KEITHLEY') and\
                self.identity['model'].endswith('2410'):
            return True
        else:
            return False

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
            data = map(float, data.lstrip().rstrip().split(','))
            data = [data[2], data[0], data[1]]
        except:
            warnings.warn('Could not read from Keithley.')
        return data

    def __del__(self):
        self.output('OFF')
        self.ser.close()
        print 'Keithley on', self.ser.name, 'released.'

    def set_i_range(self, val):
        pass

    def output(self, mode='OFF'):
        if mode in ['ON', 'OFF']:
            self.write(':OUTPUT ' + mode)
            if mode is 'ON':
                self.output_on = True
            elif mode is 'OFF':
                self.output_on = False
        else:
            print "Expecting 'ON' or 'OFF'."

    def set_v(self, V=0):
        self.write(':SOUR:VOLT '+str(V))

    def set_i(self, I=0):
        self.write(':SOUR:CURR '+str(I))

    def close(self):
        self.plotting.clear()
        self.capturing.clear()
        self.__del__

    from capture_methods import capture, _capture, stop_capture
    from plot_methods import _plot_data, stop_plotting, plot_data

if __name__ == '__main__':
    if sys.platform == 'darwin':
        k = Keithley('/dev/tty.PL2303-00001014')
    elif sys.platform == 'win32':
        k = Keithley()
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
    time.sleep(1)
    print k.read()
    k.output('OFF')
    del k
