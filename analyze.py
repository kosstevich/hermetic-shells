from data import Data
import statistics
import tabulate

class Fragment:
    def __init__(self, fragment:list):
        self.data = fragment
        # print(self._get_activity_list("a_i131"))

    def calc_fields(self):
        #TODO
        a_i131_list = self._get_activity_list("a_i131")
        a_cs134_list = self._get_activity_list("a_cs134")
        a_cs136_list = self._get_activity_list("a_cs136")
        a_cs137_list = self._get_activity_list("a_cs137")
        a_xe133_list = self._get_activity_list("a_xe133")
        a_mn54_list = self._get_activity_list("a_mn54")

        #print(a_i131_list)
        self.a_i131_amean = statistics.mean(a_i131_list)      # Arithmetic mean activity I^131
        self.a_cs134_amean = statistics.mean(a_cs134_list)
        self.a_cs136_amean = statistics.mean(a_cs136_list)
        self.a_cs137_amean = statistics.mean(a_cs137_list)
        self.a_xe133_amean = statistics.mean(a_xe133_list)
        self.a_mn54_amean = statistics.mean(a_mn54_list)
    
    def _get_activity_list(self, activity:str):
        activity_list = []
        for i in range(0,len(self.data)):
            if self.data[i].__dict__[activity] == 'н/н':
                activity_list.append(0)
            else:
                activity_list.append(self.data[i].__dict__[activity])
        return activity_list
    
    def print(self):
        ls = []
        for i in range(0,len(self.data)):
            ls.append(self.data[i].to_list())
        print(tabulate.tabulate(ls))

class Analyze:
    def __init__(self):
        self.data = Data()
        self.fragments = []

    def divide(self):
        intervals = [[1,102]] # [[start id1 interval, end id1 interval]]
        #TODO generation intervals list

        intervals_data = self.data.divide_into_intervals(intervals)
        for i in range(0,len(intervals_data)):
            fragment = Fragment(intervals_data[i])
            fragment.print()
            self.fragments.append(fragment)

    def analyze(self):
        for i in range(0,len(self.fragments)):
            self.fragments[i].calc_fields()
        
