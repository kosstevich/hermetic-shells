from data import Data
from fragment import Fragment
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

class Penal:
    def __init__(self,df):
        self.fragments = []
        self.data = df
        self.cassetes = df.iloc[np.where(df["Name"]!="Холостая")].reset_index(drop=True)

    def divide_into_fragments(self, intervals_delta:list): # 2-dimensional list of periods, e.g. [[a,b],[b,c]]
        for i in range(0,len(intervals_delta)):
            a = intervals_delta[i][0]
            b = intervals_delta[i][1]
            self.fragments.append(Fragment(self.cassetes.iloc[np.where((self.cassetes["Id1"] >= a) & (self.cassetes["Id1"] <= b))]))
            print(self.fragments[i].df)

    def analyze(self):
        for i in range(0,len(self.fragments)):
            self.fragments[i].check()

    def check_distribution(self):
        pass