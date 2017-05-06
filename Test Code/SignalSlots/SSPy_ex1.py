import sys
from time import time
from PyQt4.QtCore import *


class A(QObject):
    def __init__(self):
        QObject.__init__(self)

    def afunc(self):
        self.emit(SIGNAL("doSomePrinting()"))

    def bfunc(self):
        print "Hello World!"


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    a = A()
    QObject.connect(a, SIGNAL("doSomePrinting()"), a.bfunc)
    a.afunc()
    sys.exit(app.exec_())