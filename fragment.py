import numpy as np
import pandas as pd

class Fragment:
    def __init__(self, df):
        self.df = df
        self.non_hermetic = {} # [[dfrow,criterium],...]

    def check(self): # RD_6.7.1.5
        criteriums = ["I-131","Cs-134","Cs-137","Cs-136","Xe-133"]
        #criteriums = ["I-131"]
        non_hermetic = {}

        for i in range(0,len(criteriums)):
            df = self.df
            a_mean = df[criteriums[i]].mean()
            a_corosion_mean = df["Mn-54"].mean()
            a_std = df[criteriums[i]].std()
            a_corosion_std = df["Mn-54"].std()

            for j in range(0,len(df)):
                if (not self._isHermetic(df[criteriums[i]].iloc[j], a_mean, a_std, len(df))) and (pd.notna(df[criteriums[i]].iloc[j])):
                    cassete = df["Id1"].iloc[j]
                    non_hermetic[cassete] = criteriums[i]
                    #print(df.index[df['Id1']==df["Id1"].iloc[j]].to_list()[0])
                    #df = df.drop(df.index[df['Id1']==df["Id1"].iloc[j]].to_list()[0])
        
        print(non_hermetic)

    def _isHermetic(self, activity, mean, std, n):
        student = {2:12.7, 3:4.3, 4:3.18, 5:2.78, 6:2.57, 7:2.45, 8:2.36, 9:2.31, 10:2.26}
        return activity <= mean+student.get(n,3)*std