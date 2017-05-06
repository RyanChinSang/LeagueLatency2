import admin as wpa
import pyqtgraph as pg
import os
import sys
import numpy as np
import pypingn
from pyqtgraph.Qt import QtCore, QtGui
import rccauto

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

pg.mkQApp()
rccauto.gen()

# Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiMainWindow = os.path.join(path, 'LL.ui')
WindowTemplate, W1TemplateBaseClass = pg.Qt.loadUiType(uiMainWindow)
uiDialog1 = os.path.join(path, 'LL2.ui')
Dialog1Template, D1TemplateBaseClass = pg.Qt.loadUiType(uiDialog1)

xar = []
yar = []
sampleinterval = 0.0001
timewindow = 1.
state = 0
servers = {'North America': '104.160.131.3', 'Latin America North': '192.168.0.1'}


class MainWindow(W1TemplateBaseClass):
    global state

    # Graphing Stuff for MainWindow:
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        global sampleinterval, timewindow, xar, yar
        W1TemplateBaseClass.__init__(self)
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.toolButton.clicked.connect(self.handle_dialog1)
        self.ui.pushButton_pause.clicked.connect(self.handle_pause)
        self.ui.comboBox.activated.connect(self.handle_cb1)
        # self.ui.plotArea = self.DynamicPlotter()
        # self.ui.plotArea.plot(self.MainWindow.DynamicPlotter.getdata()[1])
        # print self.DynamicPlotter.updateplot(self.ui.plotArea)[0]
        # print self.DynamicPlotter.getdata(self.ui.plotArea)[1]
        # v =
        # vlis += [float(self.DynamicPlotter.getdata(self.ui.plotArea)[1])]
        # print vlis
        # self.ui.plotArea.plot(v)
        self.servaddr = servers[str(self.ui.comboBox.currentText())]
        self.app = QtGui.QApplication([])

        self._interval = int(sampleinterval * 1000)

        # self._bufsizey = int(timewindow / sampleinterval)
        # self.databuffery = collections.deque([self.getdata()[1]] * self._bufsizey, self._bufsizey)
        # self._bufsizex = int(timewindow / sampleinterval)
        # self.databufferx = collections.deque([self.getdata()[0]] * self._bufsizex, self._bufsizex)
        # self.y = np.zeros(self._bufsizey, dtype=np.float)
        self.y = np.array([])
        # self.x = np.zeros(self._bufsizex, dtype=np.float)
        self.x = np.array([])
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    # def show(self):
    #     self.app = QtGui.QApplication.instance().exec_()

    def getdata(self):
        # val = (str(pypingn.ping("104.160.131.3", 2)) + "\n").replace("(", "").replace(")", "")
        val = (str(pypingn.ping(self.servaddr, 2)) + "\n").replace("(", "").replace(")", "")
        x, y = val.split(',')
        return float(x), float(y)

    def updateplot(self):
        # self.databuffery.append(self.getdata()[1])
        # self.databufferx.append(self.getdata()[0])
        # self.y[:] = self.databuffery
        self.y = np.append(self.y, [self.getdata()[1]])
        # self.x[:] = self.databufferx
        self.x = np.append(self.x, [self.getdata()[0]])
        self.ui.plotArea.plot(x=self.x, y=self.y)
        # print str(self.ui.plotArea)  # <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x045D5D50>
        # self.ui.plotArea.addItem(self.x, self.y)
        self.ui.lineEdit_ping.setText("%.7f" % self.y[-1])
        self.ui.lineEdit_time.setText("%.5f" % self.x[-1])
        self.app.exec_()
        self.app.processEvents()

    def handle_dialog1(self):
        # global dia1
        # self.timer.start()
        dia1 = Dialog1(self)
        dia1.exec_()
        # dia1.show()
        # self.timer.stop()
        # return dia1

    def handle_pause(self):
        global state
        state += 1
        if state % 2 == 0:
            self.ui.pushButton_pause.setText("Pause")
            self.timer.start()
        else:
            self.ui.pushButton_pause.setText("Resume")
            self.timer.stop()

    def handle_cb1(self):
        global servers
        if self.ui.comboBox.currentText() in servers.keys():
            # print servers[str(self.ui.comboBox.currentText())]
            self.servaddr = servers[str(self.ui.comboBox.currentText())]
        else:
            # print self.ui.comboBox.currentText()
            pass


class Dialog1(D1TemplateBaseClass):
    def __init__(self, parent=None):
        D1TemplateBaseClass.__init__(self)
        self.ui = Dialog1Template()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handle_newEntry)

    def handle_newEntry(self):
        name = self.ui.lineEdit.text()
        addr = self.ui.lineEdit_2.text()
        print name, addr


def run():
    if not wpa.isUserAdmin():
        rc = wpa.runAsAdmin()
    else:
        rc = 0
        wpa.modWin(sys.executable, opt='hide')

        mainwindow = MainWindow()
        mainwindow.show()
        # mainwindow.exec_()
        QtGui.QApplication.instance().exec_()
        # QtGui.QApplication.exec_()
        pg.exit()
    return rc

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(run())

# Plot noticeably slows after 10-20 seconds because of the increasing array sizes - no buffer...
# Error everytime we exit the app... see TODO[HIGH]#05[NB1]
# External spreadsheet table functionality for importing/changing servers in /SaveData directory
