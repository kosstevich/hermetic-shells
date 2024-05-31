from analyze import Analyze
from gui import MainWindow
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    
    analyze = Analyze()
    penals = analyze.get_penals()

    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow(penals)
    analyze.control()
    
    app.exec_()
    