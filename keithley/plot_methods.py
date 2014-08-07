import matplotlib.pyplot as plt
import time


def _plot_data(self, draw_interval=1):
    self.plotting.set()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    with self.data_access:
        v_line, = ax.plot(self.data['t'], self.data['V'], '-k')
        fig.show()

    while self.plotting.is_set():
        with self.data_access:
            v_line.set_data(self.data['t'], self.data['V'])
        plt.show()
        time.sleep(draw_interval)
        self.plotting.clear()
