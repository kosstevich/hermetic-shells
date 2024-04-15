from data import Data, Fragment

class Analyze:
    def __init__(self):
        self.data = Data()
        self.fragments = []
    
    def divide(self):
        intervals = []
        #TODO
        data = data.divide_into_intervals(intervals)
        for i in range(0,len(0,len(data))):
            fragment = Fragment(data[i])
            self.fragments.append(fragment)
