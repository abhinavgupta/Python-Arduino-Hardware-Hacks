#!/usr/bin/python
# -*- coding: utf-8 -*-

# Modified version of Eli Bendersky's live plotter
# http://eli.thegreenplace.net/2009/08/07/a-live-data-monitor-with-python-pyqt-and-pyserial/
# Ozan Caglayan - 2012

import sys
import Queue

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import PyQt4.Qwt5 as Qwt

from SerialMonitor import SerialMonitorThread

def get_all_from_queue(Q):
    """ Generator to yield one after the others all items
        currently in the queue Q, without any waiting.
    """
    try:
        while True:
            yield Q.get_nowait()
    except Queue.Empty:
        raise StopIteration

class LiveDataFeed(object):
    """
        to read the most recent data and find out whether it was
        updated since the last read.

        Interface to data writer:

        add_data(data):
            Add new data to the feed.

        Interface to reader:

        read_data():
            Returns the most recent data.

        has_new_data:
            A boolean attribute telling the reader whether the
            data was updated since the last read.
    """
    def __init__(self):
        self.cur_data = None
        self.has_new_data = False

    def add_data(self, data):
        self.cur_data = data
        self.has_new_data = True

    def read_data(self):
        self.has_new_data = False
        return self.cur_data
class PlottingDataMonitor(QMainWindow):
    def __init__(self, parent=None):
        super(PlottingDataMonitor, self).__init__(parent)

        self.livefeed = LiveDataFeed()
        self.temperature_samples = []

        self.create_main_frame()

        self.data_q = Queue.Queue()
        self.error_q = Queue.Queue()
        self.serial_monitor = SerialMonitorThread(self.data_q, self.error_q)
        self.serial_monitor.start()
        self.monitor_active = True

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(1000)

    def create_plot(self):
        plot = Qwt.QwtPlot(self)
        plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time')
        plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 3, 0.1)
        plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'Temperature')
        plot.setAxisScale(Qwt.QwtPlot.yLeft, 0, 50, 5)
        plot.replot()

        curve = Qwt.QwtPlotCurve('')
        curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        pen = QPen(QColor('red'))
        pen.setWidth(2)
        curve.setPen(pen)
        curve.attach(plot)

        return plot, curve

    def create_main_frame(self):
        self.plot, self.curve = self.create_plot()

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot)

        plot_groupbox = QGroupBox('Temperature')
        plot_groupbox.setLayout(plot_layout)

        # Main frame and layout
        #
        self.main_frame = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(plot_groupbox)
        main_layout.addStretch(1)
        self.main_frame.setLayout(main_layout)

        self.setCentralWidget(self.main_frame)

    def on_timer(self):
        """ Executed periodically when the monitor update timer
            is fired.
        """
        self.read_serial_data()
        self.update_monitor()

    def update_monitor(self):
        """ Updates the state of the monitor window with new
            data. The livefeed is used to find out whether new
            data was received since the last update. If not,
            nothing is updated.
        """
        if self.livefeed.has_new_data:
            data = self.livefeed.read_data()

            self.temperature_samples.append(
                (data['timestamp'], data['temperature']))
            if len(self.temperature_samples) > 100:
                self.temperature_samples.pop(0)

            xdata = [s[0] for s in self.temperature_samples]
            ydata = [s[1] for s in self.temperature_samples]

            self.plot.setAxisScale(Qwt.QwtPlot.xBottom, xdata[0], max(20, xdata[-1]))
            self.curve.setData(xdata, ydata)
            self.plot.replot()


    def read_serial_data(self):
        """ Called periodically by the update timer to read data
            from the serial port.
        """
        qdata = list(get_all_from_queue(self.data_q))
        if len(qdata) > 0:
            data = dict(timestamp=qdata[-1][1],
                        temperature=float(qdata[-1][0]))
            #print qdata[-1][0]
            self.livefeed.add_data(data)

def main():
    app = QApplication(sys.argv)
    form = PlottingDataMonitor()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
