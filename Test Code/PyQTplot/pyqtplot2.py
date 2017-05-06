# Original: https://github.com/ap--/python-live-plotting/blob/master/plot_pyqtgraph.py
# Issue: cannot get plot to embed into UI, check:
# http://stackoverflow.com/questions/41679063/live-plotting-with-pyqtgraph-in-pyqt4

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import collections
import numpy as np
import admin as admin
import pypingn
from PyQt4 import QtCore, QtGui
import sys

# TODO: use designerExample.py as template to utilize LL.ui


class DynamicPlotter(QtGui.QWidget):
    def __init__(self, sampleinterval=0.001, timewindow=10., size=(720, 480)):
        super(DynamicPlotter, self).__init__()
        self.init_ui()
        self.qt_connections()
        self.plotcurve = pg.PlotCurveItem()
        self.plotwidget.addItem(self.plotcurve)
        # self.amplitude = 10
        # self.t = 0
        self.updateplot()
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsizey = int(timewindow/sampleinterval)
        self.databuffery = collections.deque([self.getdata()[1]] * self._bufsizey, self._bufsizey)
        self._bufsizex = int(timewindow / sampleinterval)
        self.databufferx = collections.deque([self.getdata()[0]] * self._bufsizex, self._bufsizex)
        self.y = np.zeros(self._bufsizey, dtype=np.float)
        self.x = np.zeros(self._bufsizex, dtype=np.float)
        # PyQtGraph stuff
        # self.app = QtGui.QApplication([])
        # self.plt = pg.plot(title='Pinging to 104.160.131.3')
        # self.plt.resize(*size)
        # self.plt.showGrid(x=True, y=True)
        # self.plt.setLabel('left', 'Latency', 'ms')
        # self.plt.setLabel('bottom', 'time', 's')
        # self.curve = self.plt.plot(self.x, self.y, pen=(255, 0, 0))
        # QTimer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def getdata(self):
        val = (str(pypingn.ping("104.160.131.3", 2)) + "\n").replace("(", "").replace(")", "")
        # val = (str(pypingn.ping("192.168.0.1", 2)) + "\n").replace("(", "").replace(")", "")
        x, y = val.split(',')
        return float(x), float(y)

    def updateplot(self):
        self.databuffery.append(self.getdata()[1])
        self.databufferx.append(self.getdata()[0])
        self.y[:] = self.databuffery
        self.x[:] = self.databufferx
        self.plotcurve.setData(self.x, self.y)
        self.app.processEvents()

    # def show(self):
    #     self.app.exec_()

    def init_ui(self):
        self.setWindowTitle('Sinus')
        hbox = QtGui.QVBoxLayout()
        self.setLayout(hbox)
        self.plotwidget = pg.PlotWidget()
        hbox.addWidget(self.plotwidget)
        self.increasebutton = QtGui.QPushButton("Increase Amplitude")
        self.decreasebutton = QtGui.QPushButton("Decrease Amplitude")
        hbox.addWidget(self.increasebutton)
        hbox.addWidget(self.decreasebutton)
        self.setGeometry(10, 10, 1000, 600)
        self.show()

    def qt_connections(self):
        pass
        # self.increasebutton.clicked.connect(self.stub())
        # self.decreasebutton.clicked.connect(self.stub())

    def stub(self):
        pass

def run():
    if not admin.isUserAdmin():
        rc = admin.runAsAdmin()
    else:
        rc = 0
        app = QtGui.QApplication(sys.argv)
        app.setApplicationName('Sinuswave')
        # admin.modWin(sys.executable, opt='hide')
        m = DynamicPlotter(sampleinterval=0.0001, timewindow=1.)
        # m.show()
        app.exec_()
    return rc

if __name__ == '__main__':
    sys.exit(run())

