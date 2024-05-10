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
        for i in range(0,len(self.data.penals)):
            self.penals.append(Penal(self.data.penals[i]))

    def control(self):
        print(self.penals[0].cassetes)
        intervals_delta = [[40,102]] # Hardcode, _get_intervals() in future
        self.penals[0].divide_into_fragments(intervals_delta)
        self.penals[0].analyze()
        # for i in range(0,len(self.penals)):
        #     intervals_delta = self._get_intervals()
        #     self.penals[i].divide_into_fragments(intervals_delta)
        #     self.penals[i].analyze()

    def _get_intervals(self):
        pass    