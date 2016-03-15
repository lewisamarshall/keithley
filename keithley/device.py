import serial
from serial.tools.list_ports import comports
import threading


class Device(object):

    port = None
    timeout = 1.

    def __init__(self, port=None, timeout=1):
        self.timeout = timeout
        if port is None:
            self.port = self._port_search()
        else:
            self.port = port
        self.port = 'COM7'
        self._link = serial.Serial(self.port, timeout=self.timeout)

        # Set up access control.
        self._lock = threading.Lock()

        # Flush the serial port and clear all errors from instrument.
        self.flush()
        self.reset()
        self._verify()
        print 'Keithley on', self.port, 'initialized.'

        #Set up for operation.
        # self.clear_errors()
        # self.clear_buffer()
        # self.beep('OFF')
        # self.set_term('FRONT')
        # self.write(':SENS:AVER:STAT 0')
        # self.write(':SENS:FUNC:ON "CURR", "VOLT"')
        # self.write(':FORM:ELEM VOLT, CURR, TIME')

    def flush(self):
        self._link.flush()

    def reset(self):
        self._write('*rst')

    def _port_search(self):
        print 'Automatically detecting COM ports.'
        ports = list(comports())
        print 'Detected %i ports.' % len(ports)
        port = ports[0][0]
        print 'Trying port ' + port + '.'
        return port

    def _write(self, command):
        with self._lock:
            self._link.write(command+'\n')

    def _readline(self):
        with self._lock:
            return self._link.readline()

    def identity(self):
        self._write('*idn?')
        idn_str = self._readline()
        if not idn_str:
            raise RuntimeError('No identification.')
        else:
            idn_str = idn_str.split(',')
        ID = {'make': idn_str[0],
              'model': idn_str[1],
              'serial': idn_str[2],
              'date': idn_str[3]
              }
        return ID

    def _verify(self):
        """Verify the identity of the device."""
        ID = self.identity()
        assert ID['make'] == 'KEITHLEY INSTRUMENTS INC.', 'Device is not a Keithley.'
        assert ID['model'] == 'MODEL 2410', 'Device is not a 2410 model.'
        return True

    def clear_errors(self):
        self.write('*cls')

if __name__ == '__main__':
    dev = Device()
    print dev.identity()
