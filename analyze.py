from data import Data
from fragment import Penal
import numpy as np

class Analyze:
    def __init__(self):
        filename = input("Введите имя файла(data/sample-data.ods по умолчанию)")
        if filename == "":
            self.data = Data()
        else:
            self.data = Data(filename)
        
        self.penals = []
        self.penals_intervals = {}
        for i in range(0,len(self.data.penals)):
            self.penals.append(Penal(self.data.penals[i], self.data.penals_values[i]))
            print("Пенал:",self.data.penals_values[i])
            print("Значения для ТВС:")
            print(self.penals[i].cassetes)

    def control(self): #TODO many penals
        for i in range(0,len(self.data.penals_values)):
            intervals_delta = self._get_intervals(self.data.penals_values[i])
            #intervals_delta = [[1,40],[40,102]]
            self.penals_intervals[int(self.data.penals_values[i])] = intervals_delta
            
            print("Пенал %d:" % self.data.penals_values[i])
            self.penals[i].divide_into_fragments(intervals_delta)

            self.penals[i].analyze()

        # for i in range(0,len(self.data.penals_values)):

    def _get_intervals(self, interval_id):
        n = int(input("Введите количество интервалов для пенала %d: " % interval_id))
        intervals_delta = []
        for i in range(0,n):
            a = int(input("Введите левую границу интервала %d: " % (i+1)))
            b = int(input("Введите правую границу интервала %d: " % (i+1)))
            intervals_delta.append([a,b])
        print()
        return intervals_delta 
    
    def recheck(self): #TODO
        pass
