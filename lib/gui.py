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
    def __init__(self, parent=None):
        sns.set(style="whitegrid", context="paper")
        self.fig = plt.figure(figsize=(15, 10))
        self.axes = self.fig.add_subplot(111)
        #self.draw_plot(df, axe_x, axe_y, type, title)

        super(PlotData, self).__init__(self.fig)
    
    def draw_plot(self, df, axe_x="Id1", axe_y="I-131", type = "barplot", title=None):
        self.axes.cla()
        getattr(sns,type)(data=df, x=axe_x, y=axe_y, ax=self.axes)
        plt.title(label=title, fontsize=16)

class PenalWidget(QtWidgets.QWidget):
    def __init__():
        pass

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self.resize(1200,900)
        self.model=model

        self.id = 0
        self.title = ""
        self.axe_y = "I-131"

        self.sc = PlotData(self)

        layout = QtWidgets.QHBoxLayout()
        self.penal_menu = QtWidgets.QWidget()

        for i in range(0,len(self.model.data.penals_id)):
            btn_name = "Пенал %s" % self.model.data.penals_id[i]
            penal_btn = QtWidgets.QPushButton(btn_name)
            penal_btn.released.connect(lambda id=i, name=btn_name: self.change_penal(title = name, id = id))
            layout.addWidget(penal_btn)

        self.criterium = QtWidgets.QComboBox()
        self.criterium.addItems(["I-131", "Cs-134", "Cs-137", "Cs-136", "Xe-133","Mn-54"])
        self.criterium.activated[str].connect(lambda axe_y=str: self.update_plot(axe_y=axe_y))

        layout.addWidget(self.criterium)
        self.penal_menu.setLayout(layout)

        toolbar = NavigationToolbar(self.sc, self)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(toolbar)
        self.layout.addWidget(self.sc)
        self.layout.addWidget(self.penal_menu)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def change_penal(self, title, id):
        self.title = title
        self.id = id
        self.update_plot()

    def update_plot(self, axe_x="Id1", axe_y=None, type = "barplot"):
        if axe_y: self.axe_y = axe_y
        if self.title != "":
            self.sc.draw_plot(self.model.penals[self.id].data, axe_x=axe_x, axe_y=self.axe_y, type=type, title=self.title)
            self.sc.draw()