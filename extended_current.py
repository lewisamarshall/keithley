from keithley import keithley

file = 'itp.csv'

k = Keithley('COM6')
k.write(':SOUR:FUNC:MODE CURR')
k.write(':SOUR:CURR:MODE FIX')
k.write(':SENS:FUNC:CONC 1')
k.write(':SENS:VOLT:RANG 1000')
k.write(':SENS:VOLT:RANG:AUTO 1')
k.write(':SENS:VOLT:PROT 1000')
k.write(':SENS:CURR:PROT 1')
k.write(':SENS:VOLT:NPLC 1')
k.write(':SENS:AVER:STAT 0')
k.write(':SOUR:CLE:AUTO OFF')
k.write(':SOUR:CURR:RANG .01')
k.write(':SOUR:CURR:RANG:AUTO 1')
current = .0005
k.set_i(current)

k.output('ON')
k.capture(2000, file, 'wb')
k.output('OFF')
del k
