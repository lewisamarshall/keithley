import time
import keithley.Keithley
import csv

k = keithley.Keithley()
k._write(':SENS:FUNC:ON "CURR", "VOLT"')
k.mode('VOLT')
k._write(':SENS:CURR:PROT .001')

epoch = time.time()
voltages = [500, -500]

try:
    with open('temp.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'voltage (V)', 'current (A)'])
        for v in voltages:
            k.target(voltage=v)
            k.active(True)
            for i in range(100):
                data = k.read()
                t = time.time()-epoch
                writer.writerow([t, data['voltage'], data['current']])
                time.sleep(1)
finally:
    k.active(False)
