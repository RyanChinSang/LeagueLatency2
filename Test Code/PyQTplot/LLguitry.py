import admin as wpa
import pyqtgraph as pg
import os
import sys
from pyqtgraph.Qt import QtCore, QtGui


pg.mkQApp()

# Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiMainWindow = os.path.join(path, 'LL.ui')
WindowTemplate, W1TemplateBaseClass = pg.Qt.loadUiType(uiMainWindow)
uiDialog1 = os.path.join(path, 'LL2.ui')
Dialog1Template, D1TemplateBaseClass = pg.Qt.loadUiType(uiDialog1)

# app = QtGui.QApplication(sys.argv)

class MainWindow(W1TemplateBaseClass):
    def __init__(self, parent=None):
        W1TemplateBaseClass.__init__(self)
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.toolButton.clicked.connect(self.handleDialog1)

    def handleDialog1(self):
        dia1 = Dialog1(self)
        # print str(dir(dia1))
        print "start"
        # dia1.exec_()
        # dia1.setVisible(True)
        dia1.showNormal()
        # dia1.showEvent(QtCore.QEvent.spontaneous())
        # dia1.open()
        print dia1.result()
        print "end"


class Dialog1(D1TemplateBaseClass):
    def __init__(self, parent=None):
        D1TemplateBaseClass.__init__(self)
        self.ui = Dialog1Template()
        self.ui.setupUi(self)


def run():
    global app
    if not wpa.isUserAdmin():
        rc = wpa.runAsAdmin()
    else:
        rc = 0
        # wpa.modWin(sys.executable, opt='hide')
        mainwindow = MainWindow()
        mainwindow.show()
        QtGui.QApplication.instance().exec_()
        # print str(app.exec_)
        # print str(app.exec_)
    return rc

# Start Qt event loop unless running in interactive mode or using pyside.
# if __name__ == '__main__':
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         sys.exit(run())
if __name__ == "__main__":
    # app = QtGui.QApplication(sys.argv)
    # mainwindow = MainWindow()
    # mainwindow.show()
    # sys.exit(app.exec_())
    sys.exit(run())
