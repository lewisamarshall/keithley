import keithley

file = 'C1b_exp5.4_102014.csv'

k = keithley.Keithley()
k.write(':SOUR:FUNC:MODE CURR')
k.write(':SOUR:CURR:MODE FIX')
k.write(':SENS:VOLT:RANG 1000')
k.write(':SENS:VOLT:RANG:AUTO 1')
k.write(':SENS:VOLT:PROT 1100')
k.write(':SENS:CURR:PROT 1')
k.write(':SENS:VOLT:NPLC 1')
k.write(':SOUR:CLE:AUTO OFF')
k.write(':SOUR:CURR:RANG .01')
k.write(':SOUR:CURR:RANG:AUTO 1')

current = 0.0003
k.set_i(current)

k.output('ON')
k.capture(2000, file, 'wb')
k.show_gui()
k.stop_capture()
k.output('OFF')
del k
