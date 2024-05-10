import pandas as pd
import numpy as np

class Data:
    def __init__(self, filename:str = "data/sample-data.ods", sheet_name:str = "Лист1"):
        pd.set_option('display.max_rows', None)
        pd.set_option('future.no_silent_downcasting', True)
        try:
            self.input_data, self.penals, self.cassetes = self._clear_data(pd.read_excel(filename, sheet_name))
            #print(self.input_data)
            #print(self.cassetes)
            #print(self.penals)
        except FileNotFoundError:
            print("Указанный файл не существует")
        except PermissionError:
            print("У вас нет прав на чтение данного файла")        
        
    def _clear_data(self, df):
        """На текущий момент данные очищаются под конкретный шаблон из пробных данных(КГО 5 блок 2019).
        В дальнейшем необходимо утвердить шаблон входных данных для удобного использования и внести соответствующие изменения в структуру"""

        df = df.iloc[:,0:14]
        df.rename(columns = {
            "№":"Id1",
            "№ п/п по программе":"Id2",
            "Код  и номер кассеты":"Name",
            "Индекс и номер ПС СУЗ":"Index",
            "Коорд. выгр. яч. акт. зоны ":"Coordinates",
            "Дата":"DateTime",
            "к-во кампаний":"Age",
            "Номер пенала":"IdPenal"}, inplace = True)

        for i in range(0, len(df.columns.to_list())):
            column = df.columns.to_list()[i]
            df.replace({column:"-"}, np.NaN, inplace=True)
            df.replace({column:"н/н"}, np.NaN, inplace=True)
        
        df["Age"]=df["Age"].fillna(0.0).astype(int)
        df["IdPenal"]=df["IdPenal"].fillna(0.0).astype(int)
        df["Id2"]=df["Id2"].fillna(0.0).astype(int)

        repeat = df.loc[df["Id1"]=="Повторное КГО"].index[0]
        df = df.iloc[:repeat]
        input_data = df

        penal_values = df["IdPenal"].unique()
        penals = []

        for i in range(0,len(penal_values)):
            penal = penal_values[i]
            if penal == 0: continue
            d = df[df.IdPenal==penal]
            d = d.reset_index(drop=True)
            penals.append(d)
        
        cassetes = input_data.dropna(subset=["Id1"])
        cassetes = cassetes.reset_index(drop=True)
        return input_data, penals, cassetes