from LLplotter import DynamicPlotter
import admin as wpa
import sys


def run():
    if not wpa.isUserAdmin():
        rc = wpa.runAsAdmin()
    else:
        rc = 0
        # wpa.modWin(sys.executable, opt='hide')
        m = DynamicPlotter(sampleinterval=0.001, timewindow=10.)
        # print m.y
        # print collections.deque([self.getdata()[1]] * self._bufsizey, self._bufsizey)
        print "m.app = " + str(m.app)  # <PyQt4.QtGui.QApplication object at 0x02C6E2B0>
        print "m.plt = " + str(m.plt)  # <pyqtgraph.graphicsWindows.PlotWindow object at 0x05344C60>
        # print "m.databuffery = " + str(m.databuffery)
        print "m.x = " + str(m.x)  # [ 0.  0.  0. ...,  0.  0.  0.] (updates from right on updateplot)
        print "m.curve = " + str(m.curve)  # <pyqtgraph.graphicsItems.PlotDataItem.PlotDataItem object at 0x05344DF0>
        # print "m.databufferx = " + str(m.databufferx)
        print "m.timer = " + str(m.timer)  # <PyQt4.QtCore.QTimer object at 0x05B9E170>
        print "m.y = " + str(m.y)  # [ 0.  0.  0. ...,  0.  0.  0.] (updates from right on updateplot)
        m.show()
    return rc

if __name__ == '__main__':
    sys.exit(run())