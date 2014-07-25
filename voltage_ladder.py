from keithley import keithley
import numpy

v = numpy.linspace(0,500, 11)
file = 'ladder.csv'

k = keithley('COM7')
k.write(':SENS:CURR:RANG 1e-6')
k.write(':SENS:CURR:RANG:AUTO 1')
k.write(':SENS:CURR:PROT .001')
k.write(':SENS:CURR:NPLC 2')
k.write(':SENS:AVER:STAT 0')
k.write(':SOUR:CLE:AUTO OFF')
k.write(':SOUR:VOLT:RANG 1100.0')
k.write(':SOUR:VOLT:RANG:AUTO 1')

k.output('ON')
for idx, voltage in enumerate(v):
    k.set_v(voltage)
    if idx==0:
        k.capture(10, file, 'wb')
    else:
        k.capture(10, file, 'ab')
k.output('OFF')
del k
