from device import Device

class Keithley(Device):

    def _toggle(self, command, state):
        if state is True:
            self._write(command + ' ON')
        elif state is False:
            self._write(command + ' OFF')
        elif state is None:
            pass
        else:
            raise RuntimeError('Unexpected option.')

    def _command(self, register, state):
        if state is not None:
            self._write('{} {}'.format(register, state))
        else:
            self._write('{}?'.format(register))
            return self._readline()

    def setup(self):
        self.clear_errors()
        self.clear_buffer()
        self.beep(False)
        self.concurrent(True)
        self.set_term('FRONT')

        self.write(':SENS:AVER:STAT 0')
        self.write(':SENS:FUNC:ON "CURR", "VOLT"')
        self.write(':FORM:ELEM VOLT, CURR, TIME')

    def clear_buffer(self):
        self.write(':TRAC:CLE')

    def concurrent(self, state=None):
        self._toggle('SENS:FUNC:CONC')

    def beep(self, state=None):
        self._toggle(':SYST:BEEP:STATE', state)

    def set_term(self, loc = 'FRONT'):
        self._write(':ROUT:TERM '+loc)

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
        self._write('READ?')
        data = self._readline()
        data = map(float, data.lstrip().rstrip().split(','))
        data = {'voltage':data[0], 'current':data[1]}
        return data

    def __del__(self):
        self.active(False)

    def mode(self, state=None):
        self._command('SOUR:FUNC:MODE', state)

    def target(self, voltage=None, current=None):
        if voltage is not None:
            self._command(':SOUR:VOLT', str(voltage))
        if current is not None:
            self._command(':SOUR:CURR', str(current))

    def active(self, state=None):
        self._toggle(':OUTPUT', state)

    def set_v(self, V=0):
        self.write(':SOUR:VOLT '+str(V))

    def set_i(self, I=0):
        self.write(':SOUR:CURR '+str(I))

    def close(self):
        self.__del__

if __name__ == '__main__':
    import time
    k = Keithley()
    k._write(':SENS:FUNC:ON "CURR", "VOLT"')
    k.identity()
    k.beep(False)
    k.mode('VOLT')
    k.target(voltage=100)
    k.active(True)
    for i in range(10):
        time.sleep(1)
        print k.read()
    k.active(False)
