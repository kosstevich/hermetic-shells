import pandas as pd
import numpy as np

class Data:
    def __init__(self, filename:str = "data/sample-data.ods", sheet_name:str = "Лист1"):
        pd.set_option('display.max_rows', None)
        try:
            self.input_data, self.data, self.cassetes = self._clear_data(pd.read_excel(filename, sheet_name))
            print(self.cassetes)
        except FileNotFoundError:
            print("Указанный файл не существует")
        except PermissionError:
            print("У вас нет прав на чтение данного файла")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        
        
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
            df[column].replace("-", np.NaN, inplace=True)
            df[column].replace("н/н", np.NaN, inplace=True)
        
        df["Age"]=df["Age"].fillna(0.0).astype(int)
        df["IdPenal"]=df["IdPenal"].fillna(0.0).astype(int)
        df["Id2"]=df["Id2"].fillna(0.0).astype(int)

        input_data = df
        data = df
        repeat = df.loc[df["Id1"]=="Повторное КГО"].index[0]
        data = data.iloc[:repeat]
        
        cassetes = data.dropna(subset=["Id1"])
        cassetes = cassetes.reset_index(drop=True)
        
        return input_data, data, cassetes
    
    def divide_into_intervals(self, intervals_delta:list): # 2-dimensional list of periods, e.g. [[a,b],[b,c]]
        intervals = []
        for i in range(0,len(intervals_delta)):
            intervals.append(self.cassetes.iloc[intervals_delta[i][0]:intervals_delta[i][1]])
        return intervals