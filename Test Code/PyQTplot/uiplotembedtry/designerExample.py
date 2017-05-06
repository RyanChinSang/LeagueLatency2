# -*- coding: utf-8 -*-
"""
Simple example of loading UI template created with Qt Designer.

This example uses uic.loadUiType to parse and load the ui at runtime. It is also
possible to pre-compile the .ui file using pyuic (see VideoSpeedTest and 
ScatterPlotSpeedTest examples; these .ui files have been compiled with the
tools/rebuildUi.py script).
"""
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os
from LLplotter import DynamicPlotter
import admin as admin
import sys

pg.mkQApp()

# Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'designerExample.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class MainWindow(TemplateBaseClass):  
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.setWindowTitle('pyqtgraph example: Qt Designer')
        
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.plotBtn.clicked.connect(self.plot)
        
        self.show()
        
    def plot(self):
        self.ui.plot.plot([1, 7, 5, 9], clear=True)
        # m = DynamicPlotter(sampleinterval=0.001, timewindow=10.)
        # m.curve()
        # print m.rety()
        # m.show()
        # m.curve()

def run():
    if not admin.isUserAdmin():
        rc = admin.runAsAdmin()
    else:
        rc = 0
        win = MainWindow()
        win.show()
        QtGui.QApplication.instance().exec_()
    return rc

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(run())
