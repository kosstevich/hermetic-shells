import pandas as pd
import numpy as np

class Data:
    '''
    Класс предварительной обработки данных
    Используется для получения и очистки данных из таблицы .ods 
    '''
    def __init__(self, filename:str):
        pd.set_option('display.max_rows', None)
        pd.options.display.float_format ='{:,.8f}'.format
        #pd.set_option('future.no_silent_downcasting', True)
        try:
            self.input_data, self.penals, self.penals_id, self.cassetes = self._clear_data(pd.read_excel(filename))
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

        #repeat = df.loc[df["Id1"]=="Повторное КГО"].index[0]
        #df = df.iloc[:repeat]
        df = df.dropna(subset=["Id1"])
        df = df.reset_index(drop=True)
        df["Id1"]=df["Id1"].astype(int)

        input_data = df

        penals_id = df["IdPenal"].unique()
        penals_id = penals_id[~np.isin(penals_id, 0)]
        penals = []

        for i in range(0,len(penals_id)):
            penal = penals_id[i]
            d = df[df.IdPenal==penal]
            d = d.reset_index(drop=True)
            penals.append(d)
        
        cassetes = input_data.dropna(subset=["Id1"])
        cassetes = cassetes.reset_index(drop=True)
        cassetes["Id1"]=cassetes["Id1"].astype(int)

        print(cassetes)

        return input_data, penals, penals_id, cassetes