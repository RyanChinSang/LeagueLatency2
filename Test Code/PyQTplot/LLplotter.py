# Original: https://github.com/ap--/python-live-plotting/blob/master/plot_pyqtgraph.py

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import collections
import numpy as np
# import admin as admin
import pypingn
from PyQt4 import QtCore, QtGui
# import sys

# TODO: use designerExample.py as template to utilize LL.ui


class DynamicPlotter:

    def __init__(self, sampleinterval=0.001, timewindow=10., size=(720, 480)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsizey = int(timewindow/sampleinterval)
        self.databuffery = collections.deque([self.getdata()[1]] * self._bufsizey, self._bufsizey)
        self._bufsizex = int(timewindow / sampleinterval)
        self.databufferx = collections.deque([self.getdata()[0]] * self._bufsizex, self._bufsizex)
        self.y = np.zeros(self._bufsizey, dtype=np.float)
        self.x = np.zeros(self._bufsizex, dtype=np.float)
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])
        self.plt = pg.plot(title='Pinging to 104.160.131.3')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'Latency', 'ms')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen=(255, 0, 0))
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def getdata(self):
        val = (str(pypingn.ping("104.160.131.3", 2)) + "\n").replace("(", "").replace(")", "")
        x, y = val.split(',')
        return float(x), float(y)

    def updateplot(self):
        self.databuffery.append(self.getdata()[1])
        self.databufferx.append(self.getdata()[0])
        self.y[:] = self.databuffery
        self.x[:] = self.databufferx
        self.curve.setData(self.x, self.y)
        self.app.processEvents()

    def show(self):
        self.app.exec_()


# def run():
#     if not admin.isUserAdmin():
#         rc = admin.runAsAdmin()
#     else:
#         rc = 0
#         # admin.modWin(sys.executable, opt='hide')
#         m = DynamicPlotter(sampleinterval=0.001, timewindow=10.)
#         print "m.app = " + str(m.app)
#         print "m.plt = " + str(m.plt)
#         # print "m.databuffery = " + str(m.databuffery)
#         print "m.x = " + str(m.x)
#         print "m.curve = " + str(m.curve)
#         # print "m.databufferx = " + str(m.databufferx)
#         print "m.timer = " + str(m.timer)
#         print "m.y = " + str(m.y)
#         m.show()
#     return rc
#
# if __name__ == '__main__':
#     sys.exit(run())

