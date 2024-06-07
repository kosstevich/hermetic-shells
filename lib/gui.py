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

def error(text):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText(text)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.exec_()

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
    
    def draw_plot(self, df, axe_x="Id1", axe_y="I-131", type = "barplot", name=None):
        self.axes.cla()
        getattr(sns,type)(data=df, x=axe_x, y=axe_y, ax=self.axes)
        plt.title(label= name, fontsize=16)

class DivideWindow(QtWidgets.QWidget):

    class IntervalException(Exception):
        def __init__(self, text):
            self.txt = text

    def __init__(self,parent,id):
        super().__init__()

        self.setWindowTitle("Выборки")

        self.id = id
        self.parent = parent

        self.layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel("Введите количество выборок для пенала %s" % self.parent.name)
        self.input_n = QtWidgets.QLineEdit()
        self.btn_n = QtWidgets.QPushButton("Готово")

        self.btn_n.clicked.connect(self.add_intervals)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.input_n)
        layout.addWidget(self.btn_n)
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.layout.addWidget(self.label)
        self.layout.addWidget(widget)

        self.setLayout(self.layout)

        self.show()

    def closeEvent(self, event):
        self.parent.divide_btn.setDisabled(False)

    def add_intervals(self):
        try:
            n = int(self.input_n.text())
            if n<=0:
                raise IntervalException("Значение должно быть больше 0")
        except ValueError:
            error("Значение должно быть числом")
            self.input_n.setText("")
            return
        except IntervalException as e:
            error(e.txt)
            self.input_n.setText("")
            return

        self.i = 0
        self.intervals_delta = []
        self.n = n

        self.btn_n.setDisabled(True)
        
        self.label_interval = QtWidgets.QLabel("Введите левую и правую границы выборки 1")

        self.line_a = QtWidgets.QLineEdit()
        self.line_b = QtWidgets.QLineEdit()
        self.btn_interval = QtWidgets.QPushButton("Готово")
        self.btn_interval.clicked.connect(self.read_interval)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.line_a)
        layout.addWidget(self.line_b)
        layout.addWidget(self.btn_interval)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.layout.addWidget(self.label_interval)
        self.layout.addWidget(widget)


    def read_interval(self):
        try:
            a = int(self.line_a.text())
            b = int(self.line_b.text())

            if a<=0 or b<=0:
                raise IntervalException("Значение границы должно быть больше 0")
            if b<a:
                raise IntervalException("Значение левой границы должно быть меньше, чем значение правой")

        except ValueError:
            error("Значение должно быть числом")
            self.line_a.setText("")
            self.line_b.setText("")
            return
        except IntervalException as e:
            error(e.txt)
            self.line_a.setText("")
            self.line_b.setText("")
            return

        self.intervals_delta.append([a,b])

        self.i+=1

        self.line_a.setText("")
        self.line_b.setText("")

        if self.i==self.n:
            self.btn_interval.setDisabled(True)
            print(self.intervals_delta)
            self.parent.penal_divided(self.id, self.intervals_delta)
            self.close()

        self.label_interval.setText("Введите левую и правую границы выборки %s" % (self.i+1))
        
class PenalWindow(QtWidgets.QMainWindow):
    def __init__(self, parent, penal, name, id, intervals_delta):
        super(PenalWindow, self).__init__(parent)

        self.penal = penal
        self.penal.divide_into_fragments(intervals_delta)
        self.penal_name = name
        self.penal_id = id
        self.axe_y="I-131"

        self.fragment_id = 0

        self.setWindowTitle("Пенал %s" % self.penal_name)
        
        self.sc = PlotData(self)
        self.tool = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QHBoxLayout()
        self.fragment_menu = QtWidgets.QWidget()

        for i in range(0,len(self.penal.fragments)):
            btn_name = "Выборка %s" % (i+1)
            penal_btn = QtWidgets.QPushButton(btn_name)
            penal_btn.released.connect(lambda id=i: self.change_fragment(id = id))
            layout.addWidget(penal_btn)
        self.fragment_menu.setLayout(layout)
        
        self.criterium = QtWidgets.QComboBox()
        self.criterium.addItems(["I-131", "Cs-134", "Cs-137", "Cs-136", "Xe-133","Mn-54"])
        self.criterium.activated[str].connect(lambda axe_y=str: self.update_plot(axe_y=axe_y))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tool)
        layout.addWidget(self.criterium)

        self.toolbar = QtWidgets.QWidget()
        self.toolbar.setLayout(layout)

        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.sc)
        layout.addWidget(self.fragment_menu)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def change_fragment(self, id):
        self.fragment_id = id
        self.update_plot()
        

    def update_plot(self, axe_x="Id1", axe_y=None, type = "barplot"):
        if axe_y: self.axe_y = axe_y
        self.sc.draw_plot(self.penal.fragments[self.fragment_id].df, axe_x=axe_x, axe_y=self.axe_y, type=type, name = ("Выборка %s" % (self.fragment_id+1)))
        self.sc.draw()        

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Анализ данных КГО")

        self.model=model

        self.id = 0
        self.name = ""
        self.axe_y = "I-131"

        self.penal_title = QtWidgets.QLabel("Выбран пенал: -")

        self.sc = PlotData(self)

        layout = QtWidgets.QHBoxLayout()
        self.penal_menu = QtWidgets.QWidget()

        for i in range(0,len(self.model.data.penals_id)):
            btn_name = "Пенал %s" % self.model.data.penals_id[i]
            penal_btn = QtWidgets.QPushButton(btn_name)
            penal_btn.released.connect(lambda id=i, 
                                            name=self.model.data.penals_id[i]: self.change_penal(name = name, id = id))
            layout.addWidget(penal_btn)
        self.penal_menu.setLayout(layout)
 
        self.criterium = QtWidgets.QComboBox()
        self.criterium.addItems(["I-131", "Cs-134", "Cs-137", "Cs-136", "Xe-133","Mn-54"])
        self.criterium.activated[str].connect(lambda axe_y=str: self.update_plot(axe_y=axe_y))

        self.divide_btn = QtWidgets.QPushButton("Разделить на выборки")
        #self.divide_btn.setDisabled(True)
        self.divide_btn.clicked.connect(self.open_divide_window)
        self.divide_btn.setDisabled(True)
        
        self.tool = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tool)
        layout.addWidget(self.penal_title)
        layout.addWidget(self.criterium)
        layout.addWidget(self.divide_btn)
        
        self.toolbar = QtWidgets.QWidget()
        self.toolbar.setLayout(layout)
        
        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.sc)
        layout.addWidget(self.penal_menu)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

        self.show()

    def open_divide_window(self):
        self.divide_btn.setDisabled(True)
        self.div = DivideWindow(self, self.id)

    def penal_divided(self, id, intervals_delta):
        penal_widget = PenalWindow(self, self.model.penals[id], self.name, self.id, intervals_delta)
        penal_widget.show()
        #self.model.control(id, intervals_delta)

    def change_penal(self, name, id):
        self.divide_btn.setDisabled(False)
        self.name = name
        self.id = id
        self.update_plot()
        self.penal_title.setText("Выбран пенал: %s" % self.name)

        #self.divide_btn.setDisabled(False)

    def update_plot(self, axe_x="Id1", axe_y=None, type = "barplot"):
        if axe_y: self.axe_y = axe_y
        if self.name != "":
            self.sc.draw_plot(self.model.penals[self.id].data, axe_x=axe_x, axe_y=self.axe_y, type=type, name = ("Пенал %s" % self.name))
            self.sc.draw()