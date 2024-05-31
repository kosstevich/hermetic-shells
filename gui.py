import sys
from PyQt5 import QtCore, QtWidgets, QtGui
#matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import matplotlib.pyplot as plt

class PlotData(FigureCanvasQTAgg):

    def __init__(self, parent=None, df=None, axe_x=None, axe_y=None, type="barplot"):
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        self.draw_plot(df, axe_x, axe_y, type)

        super(PlotData, self).__init__(self.fig)
    
    def draw_plot(self, df, axe_x, axe_y, type = "barplot"):
        self.axes.cla()
        getattr(sns,type)(data=df, x=axe_x, y=axe_y, ax=self.axes)

class OpenFile():
    pass

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, penals, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(1200,900)

        self.sc = PlotData(self, df = penals[0].data, axe_x="Id1", axe_y="I-131")
        self.sc2 = PlotData(self, df = penals[1].data, axe_x="Id1", axe_y="I-131")

        toolbar = NavigationToolbar(self.sc, self)
        toolbar2 = NavigationToolbar(self.sc2, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        layout.addWidget(self.sc2)
        layout.addWidget(toolbar2)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()

    def change_plot(self):
        pass