import numpy as np
import pandas as pd

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
            self.fragments[i].df = self.fragments[i].df.reset_index(drop=True)
            print(self.fragments[i].df)

    def analyze(self):
        for i in range(0,len(self.fragments)):
            self.fragments[i].check()
            print("Выборка %d:" % (i+1))
            if self.fragments[i].non_hermetic:
                print("Негерметичные ТВС")
                print(self.fragments[i].non_hermetic)
                print(self.get_df_by_dict(self.fragments[i].non_hermetic))
                print(self.fragments[i].non_hermetic)
            if self.fragments[i].recheck:
                print("ТВС для повторной проверки:")
                print(self.get_df_by_dict(self.fragments[i].recheck))
                print(self.fragments[i].recheck)

    def get_df_by_dict(self, shells):
        keys = list(shells.keys())
        df = self.data.loc[np.where(self.data["Id1"] == keys[0])]
        for i in range(1,len(keys)):
            df = pd.concat([df,self.data.loc[np.where(self.data["Id1"] == keys[i])]], ignore_index=True)
        return df

    def add_recheck_data(self):     #TODO
        pass

    def check_distribution(self):   #TODO
        pass

class Fragment:
    def __init__(self, df):
        self.df = df
        self.non_hermetic = {} # {Id1:[criterium1,criterium2],...}
        self.recheck = {}

    def check(self): # RD_6.7.1.5
        while True:
            criteriums = ["I-131","Cs-134","Cs-137","Cs-136","Xe-133"]
            non_hermetic = {}

            for i in range(0,len(criteriums)):
                df = self.df
                a_mean = df[criteriums[i]].mean()
                a_corosion_mean = df["Mn-54"].mean()
                a_std = df[criteriums[i]].std()
                a_corosion_std = df["Mn-54"].std()

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
                self.df = self.df.loc[self.df["Id1"]!=id_remove[i]]
                self.df = self.df.reset_index(drop=True)

    def _isCriterium(self, activity, mean, std, n):
        student = {2:12.7, 3:4.3, 4:3.18, 5:2.78, 6:2.57, 7:2.45, 8:2.36, 9:2.31, 10:2.26}
        return activity <= mean+student.get(n,3)*std