import admin as wpa
import pyqtgraph as pg
import os
import sys
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtCore, QtGui
from LLplotter import DynamicPlotter

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

pg.mkQApp()

# Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiMainWindow = os.path.join(path, 'LL.ui')
WindowTemplate, W1TemplateBaseClass = pg.Qt.loadUiType(uiMainWindow)
uiDialog1 = os.path.join(path, 'LL2.ui')
Dialog1Template, D1TemplateBaseClass = pg.Qt.loadUiType(uiDialog1)


class MainWindow(W1TemplateBaseClass):
    def __init__(self, parent=None):
        W1TemplateBaseClass.__init__(self)
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.toolButton.clicked.connect(self.handle_dialog1)

    def handle_dialog1(self):
        dia1 = Dialog1(self)
        dia1.exec_()


class Dialog1(D1TemplateBaseClass):
    def __init__(self, parent=None):
        D1TemplateBaseClass.__init__(self)
        self.ui = Dialog1Template()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handle_newEntry)

    def handle_newEntry(self):
        Name = self.ui.lineEdit.text()
        Addr = self.ui.lineEdit_2.text()
        print Name, Addr


def run():
    if not wpa.isUserAdmin():
        rc = wpa.runAsAdmin()
    else:
        rc = 0
        # wpa.modWin(sys.executable, opt='hide')
        mainwindow = MainWindow()
        mainwindow.show()
        QtGui.QApplication.instance().exec_()
    return rc

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(run())
