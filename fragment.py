import numpy as np
import pandas as pd
from scipy import stats

class Penal:
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

    def analyze(self):
        #criteriums = ["I-131","Cs-134","Cs-137","Cs-136","Xe-133","Mn-54"]
        criteriums = ["I-131","Mn-54"]
        
        for i in range(0,len(criteriums)):
            print("Проверка принадлежности к одному статистическому распредлению:")
            self.check_distribution(criteriums[i])

        print("Проверка выборок:")
        for i in range(0,len(self.fragments)):
            self.fragments[i].check()
            print("Выборка %d:" % (i+1))
            if self.fragments[i].non_hermetic:
                print("Негерметичные ТВС")
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

    def check_distribution(self,criterium):   #TODO
        fragments_data = []
        fragments_length = []

        for i in range(0, len(self.fragments)):
            fragments_data.append(self.fragments[i].df[criterium].fillna(0.0).values)
            fragments_length.append(len(fragments_data[i]))
        
        #print(fragments_data)
        #print(fragments_length)
        
        m = len(fragments_data)
        subfragments = []
        subfragments_log_vars = []

        for i in range(0,len(fragments_data)):
            if len(fragments_data[i]) <= 5:
                n = np.array(fragments_data[i])
                subfragments.append([n])
                subfragments_log_vars.append([np.log(n.var())])
            else:     
                n1, n2 = self.random_generate(i, fragments_data)
                subfragments.append([n1,n2])
            
                v1 = n1.var()
                v2 = n2.var()
                subfragments_log_vars.append([np.log(v1), np.log(v2)])

        #print("subfragments: ", subfragments)
        #print("subfragments_log_vars:", subfragments_log_vars)
        check_vars_result = self.check_vars(len(self.cassetes), m, subfragments, subfragments_log_vars,criterium)
        print(check_vars_result)

        # if err:
        #     return None
        # else:
        #     return "Error" 

    def random_generate(self, i, fragments_data):
        n1 = [] # subfragment1
        n2 = [] # subfragment2
        
        for j in range(0,len(fragments_data[i])):
            r = np.random.randint(0,2)
            if r == 0: n1.append(fragments_data[i][j])
            else: n2.append(fragments_data[i][j])

        while len(n1)<3 or len(n2)<3:
            n1,n2 = self.random_generate(i, fragments_data)

        return np.array(n1), np.array(n2)

    def check_vars(self, n, m, subfragments, subfragments_log_vars, criterium): #RD_ZH.7
        err = ""
        
        vl = 0
        vi = []
        vij = []
        yi = []
        y = 0
        vs = 0
        for i in range(0,m):
            v = []
            yiv = 0
            vl+=(len(subfragments[i])-1)
            vsum = 0
            for j in range(0,len(subfragments[i])):
                v.append(len(subfragments[i][j])-1)
                yiv += (len(subfragments[i][j])-1)*subfragments_log_vars[i][j]
                vsum+=(len(subfragments[i][j])-1)

            vij.append(v)
            vi.append(np.array(vsum))
            vs += vsum

            yi.append(np.array(yiv / vsum))
        
        yi = np.array(yi)
        vi = np.array(vi)

        v = vs
        y = (vi*yi)/v
        y = y.sum()

        ssh = (((yi - y)**2)*vi).sum()/(m-1)
        ssl = 0

        for i in range(0, len(subfragments_log_vars)):
            for j in range(0, len(subfragments_log_vars[i])):
                ssl+=((subfragments_log_vars[i][j] - yi[i])**2)*vij[i][j]
                
        ssl /= vl
        if ssl>=ssh:
            statistic = ssl/ssh
        else:
            statistic = ssh/ssl

        #norm = stats.norm()
        #p = norm.cdf(statistic) # cdf(x,loc=0,scale=1) loc-mena, scale=std
        #print("P(N(0,1))", p)
        result = pd.Series({"criterium": criterium,"statistic":statistic, "ssh":ssh,"ssl":ssl,"n":n, "m":m, "vl":vl, "yi":yi, "vi":vi,"vij":vij,"v":v,"y":y,})

        return result


class Fragment:
    def __init__(self, df):
        self.df = df
        self.non_hermetic = {} # {Id1:[criterium1,criterium2],...}
        self.recheck = {}

    def check(self): # RD_6.7.1.5
        criteriums = ["I-131","Cs-134","Cs-137","Cs-136","Xe-133"]
        while True:
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

    def check_distribution(self):
        pass

    def _isCriterium(self, activity, mean, std, n):
        student = {2:12.7, 3:4.3, 4:3.18, 5:2.78, 6:2.57, 7:2.45, 8:2.36, 9:2.31, 10:2.26}
        return activity <= mean+student.get(n,3)*std