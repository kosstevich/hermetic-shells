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
        self.fragments = []
        for i in range(0,len(intervals_delta)):
            a = intervals_delta[i][0]
            b = intervals_delta[i][1]
            self.fragments.append(Fragment(self.cassetes.iloc[np.where((self.cassetes["Id1"] >= a) & (self.cassetes["Id1"] <= b))]))
            self.fragments[i].df = self.fragments[i].df.reset_index(drop=True)
            print(self.fragments[i].df)
            #random_generate(self.fragments[i].df, "I-131")


    def analyze(self):
        self.output_data = {}

        print("Проверка выборок:")
        for i in range(0,len(self.fragments)):
            print("Выборка %d:" % (i+1))
            non_hermetic_df, recheck_df = self.fragments[i].check()
            #non_hermetic_df, recheck_df = self.fragments[i].check("IQR")

            self.output_data[i] = [non_hermetic_df, recheck_df]

            if not non_hermetic_df.empty:
                ext_df = self.fragments[i].get_parameters_df()
                self.output_data[i].append(ext_df)
                print("Негерметичные ТВС")
                print(non_hermetic_df)
                

            if not recheck_df.empty:
                ext_df = self.fragments[i].get_parameters_df()
                self.output_data[i].append(ext_df)
                print("ТВС для повторной проверки:")
                print(recheck_df)

            print()
        return self.output_data

    def export_data(self, filename="output.ods", writer = pd.ExcelWriter(path="otput.ods", datetime_format='DD-MM-YYYY HH:MM:SS')):
        #with pd.ExcelWriter(path=filename, datetime_format='DD-MM-YYYY HH:MM:SS') as writer:  
        sheet = "МП%s" % self.id
        self.data.to_excel(excel_writer = writer, sheet_name = sheet, index=False)

        for i in range(0, len(self.fragments)):
            sheet = "МП%s-%s" % (self.id, (i+1))

            parameters = self.fragments[i].get_parameters_df()
            parameters.to_excel(excel_writer = writer, sheet_name = sheet)

            self.fragments[i].df.to_excel(excel_writer = writer, sheet_name = sheet, index=False)

            if not self.fragments[i].non_hermetic_df.empty:
                df = pd.DataFrame(data = ["Негерметичные ТВС:"])
                df.to_excel(excel_writer=writer,sheet_name=sheet, index=False)
                self.fragments[i].non_hermetic_df.to_excel(excel_writer=writer, sheet_name=sheet, index=False)
            if not self.fragments[i].recheck_df.empty:
                df = pd.DataFrame(data = ["ТВС для повторной проверки:"])
                df.to_excel(excel_writer=writer,sheet_name=sheet, index=False)
                self.fragments[i].recheck_df.to_excel(excel_writer=writer, sheet_name=sheet, index=False)
    
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

    def check(self, method_type="3_sigma"):
        '''
        Поиск выброса "3 sigma" согласно RD_6.7.1.5
        ''' 
        df = self.df
        self.parameters = self.calc_3sigma_params(df)
        #print(pd.DataFrame.from_dict(self.parameters, orient="Index", columns=criteriums))
        self.non_hermetic_df = pd.DataFrame()
        self.recheck_df=pd.DataFrame()
        
        while True:
            remove = pd.DataFrame()
            
            for i in range(0,len(criteriums)-1):
                if method_type=="IQR":
                    a_q1 = df[criteriums[i]].quantile(q=.25)
                    a_q3 = df[criteriums[i]].quantile(q=.75)
                    a_IQR = a_q3-a_q1
                    
                    a_corosion_q1 = df[criteriums[i]].quantile(q=.25)
                    a_corosion_q3 = df[criteriums[i]].quantile(q=.75)
                    a_corosion_IQR = a_corosion_q3-a_corosion_q1

                    a_crit = (a_q3+1.7*a_IQR)
                    a_corosion_crit = (a_corosion_q3+1.7*a_corosion_IQR)
                else:
                    #Расчёт параметров
                    a_mean = df[criteriums[i]].mean()
                    a_corosion_mean = df["Mn-54"].mean()
                    a_std = df[criteriums[i]].std()
                    a_corosion_std = df["Mn-54"].std()
                    a_crit = self.crit_value(a_mean, a_std, len(df))
                    a_corosion_crit = self.crit_value(a_corosion_mean, a_corosion_std, len(df))

                crit_df = df[(df[criteriums[i]]>a_crit)].reset_index(drop=True)
                non_hermetic = crit_df[crit_df["Mn-54"]<a_corosion_crit]
                recheck = crit_df[crit_df["Mn-54"]>=a_corosion_crit]

                if not non_hermetic.empty:
                    non_hermetic["Criterium"] = criteriums[i] 
                    self.non_hermetic_df = pd.concat([self.non_hermetic_df,non_hermetic], ignore_index=True)
                
                if not recheck.empty:
                    recheck["Criterium"] = criteriums[i] 
                    self.recheck_df = pd.concat([self.recheck_df,recheck], ignore_index=True)

                remove = pd.concat([remove,crit_df["Id1"]], ignore_index=True)
            
            if remove.empty:
                break

            for i in range(0,len(remove)):
                df = df.loc[df["Id1"]!=remove[0].iloc[i]]
                df = df.reset_index(drop=True)

        return self.non_hermetic_df, self.recheck_df

    def get_parameters_df(self):
        df = pd.DataFrame.from_dict(self.parameters, orient="Index", columns=criteriums)
        return df
        
    def stat_tests(self, criterium):
        pass

    def crit_value(self, mean, std, n):
        student = {2:12.7, 3:4.3, 4:3.18, 5:2.78, 6:2.57, 7:2.45, 8:2.36, 9:2.31, 10:2.26}

        if (not pd.notna(mean)) or (not pd.notna(std)): return 0

        return mean+student.get(n,3)*std

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