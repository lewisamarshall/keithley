import keithley
import numpy
import time

v = numpy.linspace(0, 1100, 23)
file = 'temp.csv'

k = k = keithley.Keithley()
k.write(':SENS:CURR:RANG 1e-6')
k.write(':SENS:CURR:RANG:AUTO 1')
k.write(':SENS:CURR:PROT .01')
k.write(':SENS:CURR:NPLC 2')
k.write(':SENS:AVER:STAT 0')
k.write(':SOUR:CLE:AUTO OFF')
k.write(':SOUR:VOLT:RANG 1100.0')
k.write(':SOUR:VOLT:RANG:AUTO 1')

k.output('ON')
k.capture(2000, file, 'wb')
for idx, voltage in enumerate(v):
    k.set_v(voltage)
    time.sleep(10)
k.stop_capture()
k.output('OFF')
del k
