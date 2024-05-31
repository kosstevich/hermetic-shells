from PyQt5 import QtWidgets
from model import Model
from gui import MainWindow, open_file
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    filename = open_file()

    model = Model(filename)
    
    main_window = MainWindow(model)
    main_window.show()

    app.exec_()