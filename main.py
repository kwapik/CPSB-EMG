#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys

from PyQt4 import QtCore, QtGui

from numpy import arange, fft, pi, sin
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import fftpack

from core import Acquire
from peakdetect import peakdetect
from settings import settingsInit


class Window(QtGui.QMainWindow):
    """Main window class"""
    sc = None
    fc = None

    def __init__(self):
        """Calls all needed inits"""
        super(Window, self).__init__()
        settingsInit()
        self.initUI()

    def initUI(self):
        """Creates main window"""
        
        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        self.sc = SignalCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.fc = FFTCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(self.sc)
        l.addWidget(self.fc)
        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        """Plot areas"""
        
        exitAction = QtGui.QAction(
                        QtGui.QIcon('images/icon_exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        """Exit button"""
        
        acquireAction = QtGui.QAction(
                        QtGui.QIcon('images/icon_play.png'), 'Acquire', self)
        acquireAction.setShortcut('Ctrl+S')
        acquireAction.triggered.connect(self.start_acquire)
        #acquireAction.triggered.connect(sc.update_figure)
        #acquireAction.triggered.connect(fc.update_figure)

        """Acquire button"""
        
        self.toolbar = self.addToolBar('Menu')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(acquireAction)
        """Creating toolbar"""

        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('EMG controller')
        """Window parameters"""

        self.show()

    def start_acquire(self):
        """Creates Acquire instance"""
        acq = Acquire()
        QtCore.QObject.connect(acq, QtCore.SIGNAL('update_plots(PyQt_PyObject)'), self.sc.update_figure)
        QtCore.QObject.connect(acq, QtCore.SIGNAL('update_plots(PyQt_PyObject)'), self.fc.update_figure)
        acq.start()


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        #self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_figure(self):
        pass


class SignalCanvas(MyMplCanvas):
    """A canvas for signal plot."""

    def update_figure(self, output):
        print "Signal update called"
        self.axes.plot(range(1000), output, 'r')
        self.draw()


class FFTCanvas(MyMplCanvas):
    """A canvas for signal plot."""

    def update_figure(self, output):
        print "FFT update called"

        fftX = fftpack.fftfreq(len(output), d=0.1)
        fftY = fftpack.rfft(output)

        _max, _min = peakdetect(fftY, fftX, 500, 0.30)
        xm = [p[0] for p in _max]
        ym = [abs(p[1]) for p in _max]
        xn = [p[0] for p in _min]
        yn = [abs(p[1]) for p in _min]

        self.axes.hold(True)
        self.axes.bar(xm, ym, 0.02, color='r')
        self.axes.bar(xn, yn, 0.02, color='y')
        #self.axes.plot(xn, yn, 'r')

        self.draw()


def main():
    """Main function"""
    app = QtGui.QApplication(sys.argv)

    win = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
