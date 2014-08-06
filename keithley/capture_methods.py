import time
import csv
import threading
import warnings


def capture(self, t=None, filename='data.csv', mode='wb'):
    self.capture_thread = threading.Thread(
                                           target=_capture,
                                           args=(filename,
                                                 mode,
                                                 wait_time
                                                 )
                                           )
    t0 = time.time()
    dt = 0
    with open(filename, mode) as file:
        writer = csv.writer(file)
        if 'w' in mode:
            writer.writerow(['T', 'V', 'I'])
        while dt < t:
            dt = time.time()-t0
            self.data.append(self.read())
            time.sleep(0.1)
            if data[-1]:
                writer.writerow(data[-1])
    return data

def _capture(self, filename='test', mode='wb', wait_time=0.1):
    self.capturing.set()
    with open(filename, mode) as file:
        writer = csv.writer(file)
        if 'w' in mode:
            writer.writerow(['T', 'V', 'I'])
        while self.capturing.is_set():
            reading = (self.read())
            if reading:
                with self.data_access:
                    data.append(reading)
                writer.writerow(reading)
            time.sleep(wait_time)
            self.capturing.clear()


def stop_capture(self):
    self.capturing.clear()
    return None
