import sys
from PyQt5 import QtCore, QtWidgets, QtGui
#matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import matplotlib.pyplot as plt
import random

def open_file():
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Выберите входной файл', './', "Table (*.ods)")
    return filename

class PlotData(FigureCanvasQTAgg): 
    '''
    Виджет для отрисовки графиков, использующий matplotlib
    '''
    def __init__(self, parent=None, df=None, axe_x=None, axe_y=None, type="barplot"):
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        self.draw_plot(df, axe_x, axe_y, type)

        super(PlotData, self).__init__(self.fig)
    
    def draw_plot(self, df, axe_x, axe_y, type = "barplot"):
        self.axes.cla()
        getattr(sns,type)(data=df, x=axe_x, y=axe_y, ax=self.axes)

class PenalWidget(QtWidgets.QWidget):
    def __init__():
        pass

class Menu(QtWidgets.QWidget):
    def __init__():
        pass

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(1200,900)
        self.model=model

        self.sc = PlotData(self, df = self.model.penals[0].data, axe_x="Id1", axe_y="I-131")
        self.sc2 = PlotData(self, df = self.model.penals[1].data, axe_x="Id1", axe_y="I-131")

        toolbar = NavigationToolbar(self.sc, self)
        toolbar2 = NavigationToolbar(self.sc2, self)

        self.btn = QtWidgets.QPushButton("Change")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(toolbar)
        self.layout.addWidget(self.sc)
        self.layout.addWidget(self.sc2)
        self.layout.addWidget(toolbar2)

        self.btn.clicked.connect(self.change_plot)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.layout.addWidget(self.btn)

    def change_plot(self):
        types = ["lineplot","barplot"]
        i = random.randint(0,1)
        self.sc.draw_plot(self.model.penals[0].data, axe_x="Id1", axe_y="I-131", type = types[i])
        self.sc.draw()