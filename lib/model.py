from data import Data
from fragment import Penal
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class Model:
    '''
    Класс обёртка для Data и Penal
    '''
    def __init__(self, filename = "../data/sample-data.ods"):
        self.data = Data(filename)

        #plt.hist(self.data.cassetes["I-131"], bins=200)
        #plt.show()
        
        self.penals = []
        self.penals_intervals = {}
        for i in range(0,len(self.data.penals)):
            self.penals.append(Penal(self.data.penals[i], self.data.penals_id[i]))
            print("Пенал:",self.data.penals_id[i])
            print("Значения для ТВС:")
            print(self.penals[i].cassetes)

    def control(self, id, intervals_delta): #TODO many penals
        if not intervals_delta:
            intervals_delta = self._get_intervals(self.data.penals_id[id])

        self.penals_intervals[int(self.data.penals_id[id])] = intervals_delta
        
        print("Пенал %d:" % self.data.penals_id[id])
        self.penals[id].divide_into_fragments(intervals_delta)

        fragments = self.penals[id].analyze()
        return fragments

    def get_penals(self):
        return self.penals

    def _get_intervals(self, penal_id):
        n = int(input("Введите количество интервалов для пенала %d: " % penal_id))
        intervals_delta = []
        for i in range(0,n):
            a = int(input("Введите левую границу интервала %d: " % (i+1)))
            b = int(input("Введите правую границу интервала %d: " % (i+1)))
            intervals_delta.append([a,b])
        print()
        return intervals_delta 
    
    def recheck(self): #TODO
        pass