# import matplotlib.pyplot as plt
import time
import multiprocessing

plt.ion()

def plot_data(self, draw_interval=1):
    self.draw_thread = threading.Thread(
                                        target=self._plot_data,
                                        args=([draw_interval])
                                        )
    self.draw_thread.start()

def _plot_data(self, draw_interval=1):
    self.plotting.set()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    with self.data_access:
        v_line, = ax.plot(self.data['t'], self.data['V'], '-k')
        fig.show()
        print 'done with first draw'

    print self.plotting.is_set()
    while self.plotting.is_set():
        with self.data_access:
            v_line.set_data(self.data['t'], self.data['V'])
        time.sleep(draw_interval)
        fig.canvas.draw()

def stop_plotting(self):
    self.plotting.clear()
