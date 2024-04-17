from data import Data
import statistics
import tabulate

class Fragment:
    def __init__(self, fragment:list, criterium_name:str):
        self.data = fragment
        self.criterium_name = criterium_name
        self.activity_amean = None
        self.corosion_amean = None
        self.activity_stdev = None
        self.corosion_stdev = None

    def calc_fields(self):
        self.activity_list = self._get_activity_list(self.criterium_name)
        self.corosion_list = self._get_activity_list("a_mn54")

        self.activity_amean = statistics.mean(self.activity_list)      # Arithmetic mean activity (I^131 for example)
        self.corosion_amean = statistics.mean(self.corosion_list)
        self.activity_stdev = statistics.stdev(self.activity_list, self.activity_amean) # Need to check
        self.corosion_stdev = statistics.stdev(self.corosion_list, self.corosion_amean)
    
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
        print("Criterium: ", self.criterium_name)
        print("Arithmetic mean of critrium: ", self.activity_amean)
        print("Arithmetic mean of corosion: ", self.corosion_amean)
        print("Standard deviation of criterium", self.activity_stdev)
        print("Standard deviation of corosion", self.corosion_stdev)
        for i in range(0,len(self.data)):
            ls.append(self.data[i].to_list())
        print(tabulate.tabulate(ls))

class Analyze:
    def __init__(self):
        self.data = Data()
        self.fragments = []

    def divide(self):
        intervals = [[1,102]] # [[start id1 interval, end id1 interval]]
        criterium = ["a_i131", "a_cs134", "a_cs136", "a_cs137","a_xe133"]
        #TODO generation intervals list

        intervals_data = self.data.divide_into_intervals(intervals)
        for i in range(0,len(intervals_data)):
            for j in range(0,len(criterium)):
                fragment = Fragment(intervals_data[i],criterium[j])
                self.fragments.append(fragment)

    def analyze(self):
        for i in range(0,len(self.fragments)):
            self.fragments[i].calc_fields()
            for j in range(0,len(self.fragments[i].data)):
                activity = self.fragments[i].data[j].__dict__[self.fragments[i].criterium_name]
                mean = self.fragments[i].activity_amean
                stdev = self.fragments[i].activity_stdev
                
                if activity <= (mean + 3*stdev):
                    self.fragments[i].data[j].status = 0
                else:
                    corosion = self.fragments[i].data[j].a_mn54
                    mean_corosion = self.fragments[i].corosion_amean
                    stdev_corosion = self.fragments[i].corosion_stdev

                    if corosion <= (mean_corosion + 3*stdev_corosion):
                        self.fragments[i].data[j].status = 1
                    else:
                        self.fragments[i].data[j].status = -1

            self.fragments[i].print()