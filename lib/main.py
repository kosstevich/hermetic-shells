from PyQt5 import QtWidgets
from model import Model
from gui import MainWindow, open_file
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    filename = open_file()

    model = Model()
    # model.control(0)
    # model.control(1)
    #model.control(0)
    main_window = MainWindow(model)
    main_window.show()

    app.exec_()

