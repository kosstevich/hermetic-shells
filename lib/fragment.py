import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

criteriums = ["I-131","Cs-134","Cs-137","Cs-136","Xe-133", "Mn-54"]

class Penal:
    '''
    Сущность, которая отвечает за конкретный пенал СОДС 
    '''
    def __init__(self,df, id):
        self.fragments = []
        self.data = df
        self.cassetes = df.iloc[np.where(df["Name"]!="Холостая")].reset_index(drop=True)
        self.id = id

    def divide_into_fragments(self, intervals_delta:list): # 2-dimensional list of periods, e.g. [[a,b],[b,c]]
        for i in range(0,len(intervals_delta)):
            a = intervals_delta[i][0]
            b = intervals_delta[i][1]
            self.fragments.append(Fragment(self.cassetes.iloc[np.where((self.cassetes["Id1"] >= a) & (self.cassetes["Id1"] <= b))]))
            self.fragments[i].df = self.fragments[i].df.reset_index(drop=True)
            print(self.fragments[i].df)
            #random_generate(self.fragments[i].df, "I-131")


    def analyze(self):
        print("Проверка выборок:")
        for i in range(0,len(self.fragments)):
            print("Выборка %d:" % (i+1))
            #self.fragments[i].check_iqr()
            self.fragments[i].check3sigma()
            
            if self.fragments[i].non_hermetic:
                df, ext_df = self.get_data_by_dict(self.fragments[i].non_hermetic, self.fragments[i].parameters)
                print("Негерметичные ТВС")
                print(df)
                print("Расширенная информация:")
                print(ext_df)
                print()
                print(self.fragments[i].non_hermetic)

            if self.fragments[i].recheck:
                df, ext_df = self.get_data_by_dict(self.fragments[i].recheck, self.fragments[i].parameters)
                print("ТВС для повторной проверки:")
                print(df)
                print("Расширенная информация:")
                print(ext_df)
                print()

            print()
    
    def get_data_by_dict(self, shells, ext):
        keys = list(shells.keys())
        df = pd.DataFrame()

        ext_df = pd.DataFrame.from_dict(ext, orient="Index", columns=criteriums)
        
        for i in range(0,len(keys)):
            shell = self.data.loc[np.where(self.data["Id1"] == keys[i])]
            shell["Criteriums"] = str(shells[keys[i]])
            df = pd.concat([df,shell], ignore_index=True)
                
        return df, ext_df

    def check_distribution(self, criterium):
        pass

class Fragment:
    '''
    Сущность, которая отвечает за выборку 
    '''
    def __init__(self, df):
        self.df = df
        self.non_hermetic = {} # {Id1:[criterium1,criterium2],...}
        self.recheck = {}

        # plt.hist(df["I-131"], bins=len(df))
        # plt.show()
        #plt.hist(df["I-131"])
        #sns.distplot(x=self.df["I-131"], bins=1)
        #plt.show()

    def check_iqr(self):
        criteriums = ["I-131","Cs-134","Cs-137","Cs-136","Xe-133","Mn-54"]
        print("Check IQR:")
        for i in range(0,len(criteriums)-1):
            data = self.df
            Q1 = data[criteriums[i]].quantile(q=.25)
            Q3 = data[criteriums[i]].quantile(q=.75)
            IQR = Q3-Q1

            #only keep rows in dataframe that have values within 1.5\*IQR of Q1 and Q3
            data_clean = data[(data[criteriums[i]] > (Q3+1.7*IQR))]
            if not data_clean.empty:
                print(criteriums[i])
                print("Q1: ", Q1, "Q3: ", Q3)
                print("IQR:")
                print(IQR)
                print("Q3+1,5*IQR:", Q3 + 1.7*IQR)
                print("data_clean:")
                print(data_clean)

    def calc_3sigma_params(self, df):
        parameters = {
            "Activity_mean" : [], 
            "Activity_std" : [], 
            "Activity_critical" : []
        }

        for i in range(0, len(criteriums)):
            a_mean = df[criteriums[i]].mean()
            a_std = df[criteriums[i]].std()
            a_crit = self.crit_value(a_mean, a_std, len(df))
            
            parameters["Activity_mean"].append(a_mean)
            parameters["Activity_std"].append(a_std)
            parameters["Activity_critical"].append(a_crit)
        
        return parameters

    def check_3sigma(self):
        pass

    def check3sigma(self):
        '''
        Поиск выброса "3 sigma" согласно RD_6.7.1.5
        ''' 
        df = self.df
        self.parameters = self.calc_3sigma_params(df)

        while True:
            non_hermetic = {}
            
            for i in range(0,len(criteriums)-1):
                
                #Расчёт параметров
                a_mean = df[criteriums[i]].mean()
                a_corosion_mean = df["Mn-54"].mean()
                a_std = df[criteriums[i]].std()
                a_corosion_std = df["Mn-54"].std()
                a_crit = self.crit_value(a_mean, a_std, len(df))
                a_corosion_crit = self.crit_value(a_corosion_mean, a_corosion_std, len(df))

                # a_3sigma_df = df[(df[criteriums[i]]<a_crit) ]
                # print()
                # print("a_3sigma_df[%s]:"%criteriums[i])
                # print(a_3sigma_df)
                # print()
                for j in range(0,len(df)):
                    if (not self._isCriterium(df[criteriums[i]].iloc[j], a_mean, a_std, len(df))) and (pd.notna(df[criteriums[i]].iloc[j])):
                        cassete = df.iloc[j]
                        if self._isCriterium(df["Mn-54"].iloc[j], a_corosion_mean, a_corosion_std, len(df)):
                            exist = non_hermetic.get(cassete["Id1"])
                            if not exist: non_hermetic[cassete["Id1"]] = [criteriums[i]]
                            else: non_hermetic[cassete["Id1"]].append(criteriums[i])

                            exist = self.non_hermetic.get(cassete["Id1"])
                            if not exist: self.non_hermetic[cassete["Id1"]] = [criteriums[i]]
                            else: self.non_hermetic[cassete["Id1"]].append(criteriums[i])
                        else:   #TODO RD_6.7.1.9
                            exist = self.recheck.get(cassete["Id1"])
                            if not exist: self.recheck[cassete["Id1"]] = [criteriums[i]]
                            else: self.recheck[cassete["Id1"]].append(criteriums[i])
            
            if not non_hermetic:
                break

            id_remove = list(non_hermetic.keys())

            for i in range(0,len(id_remove)):
                df = df.loc[df["Id1"]!=id_remove[i]]
                df = df.reset_index(drop=True)
        

    def stat_tests(self, criterium):
        pass

    def crit_value(self, mean, std, n):
        student = {2:12.7, 3:4.3, 4:3.18, 5:2.78, 6:2.57, 7:2.45, 8:2.36, 9:2.31, 10:2.26}
        return mean+student.get(n,3)*std

    def _isCriterium(self, activity, mean, std, n):
        '''
        Проверка критерия "3 sigma"
        '''
        student = {2:12.7, 3:4.3, 4:3.18, 5:2.78, 6:2.57, 7:2.45, 8:2.36, 9:2.31, 10:2.26}
        critical_value = mean+student.get(n,3)*std
        return activity <= critical_value

def random_generate(df, criterium):
    n1 = [] # subfragment1
    n2 = [] # subfragment2
    
    for i in range(0,len(df)):
        r = np.random.randint(0,2)
        if r == 0: n1.append(df[criterium].iloc[i])
        else: n2.append(df[criterium].iloc[i])

    print("n1:")
    print(n1)
    print("n2:")
    print(n2)

    return n1,n2