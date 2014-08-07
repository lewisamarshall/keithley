import time
import csv
import threading
import warnings


def capture(self, t=None, filename='data.csv', mode='wb',
            capture_interval = 0.1):
    self.capture_thread = threading.Thread(
                                           target=_capture,
                                           args=(filename,
                                                 mode,
                                                 capture_interval
                                                 )
                                           )
    return self.capture_thread

def _capture(self, filename='test.csv', mode='wb', capture_interval=0.1):
    self.capturing.set()
    with open(filename, mode) as file:
        writer = csv.writer(file)
        if 'w' in mode:
            writer.writerow(['T', 'V', 'I'])
        while self.capturing.is_set():
            reading = (self.read())
            if reading:
                with self.data_access:
                    self.data['V'].append(reading[1])
                    self.data['I'].append(reading[2])
                    self.data['t'].append(reading[0])
                writer.writerow(reading)
            time.sleep(capture_interval)


def stop_capture(self):
    self.capturing.clear()
    return None
