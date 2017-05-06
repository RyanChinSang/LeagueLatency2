#Notes: goto howtogencode.txt

from PyQt4 import QtCore, QtGui
import sys

from LLuitry0 import Ui_MainWindow
from LLuitry1 import Ui_Dialog


class Dialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QDialog.__init__(self, parent, f)

        self.setupUi(self)


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)
        self.toolButton.clicked.connect(self.handleDialog)

    # @QtCore.pyqtSlot()
    def handleDialog(self):
        window = Dialog(self)
        window.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
