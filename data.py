from dataclasses import dataclass
from openpyxl import load_workbook
from datetime import datetime
import pandas as pd

@dataclass
class Cassete:
    id1: int = None             # №
    id2: int = None             # п/п
    name: str  = None           # Код  и номер кассеты
    coordinates: str = None     # Коорд. выгр. яч. акт. зоны 
    date_time: datetime  = None 
    companies: int = None       # Кол-во компаний
    id_pen: int = None          # Номер пенала
    a_i131: float = None        # Aктивность I^131
    a_cs134: float = None
    a_cs136: float = None
    a_cs137: float = None
    a_mn54: float = None

class Data:
    def __init__(self, filename:str, sheet_name:str = "Лист1"):
        self.input_data = pd.read_excel(filename, sheet_name=sheet_name)
        # self._read(filename, sheet_name)

    # def _read(self, filename:str, sheet_name:str = "Лист1"):
    #     table = pd.read_excel(filename)
    #     print(table)
    #     file = load_workbook(filename)
    #     sheet = file.get_sheet_by_name(sheet_name)
    #     rows = sheet.max_row

    #     for i in range(2, rows + 1):
    #         cassete = Cassete(
    #             id1 = sheet.cell(row=i, column=1).value,
    #             id2 = sheet.cell(row=i, column=2).value,
    #             name = sheet.cell(row=i, column=3).value,
    #             coordinates = sheet.cell(row=i, column=5).value,
    #             date_time = sheet.cell(row=i, column=6).value,
    #             companies = sheet.cell(row=i, column=7).value,
    #             id_pen = sheet.cell(row=i, column=8).value,
    #             a_i131 = sheet.cell(row=i, column=9).value,
    #             a_cs134 = sheet.cell(row=i, column=10).value,
    #             a_cs136 = sheet.cell(row=i, column=13).value,
    #             a_cs137 = sheet.cell(row=i, column=11).value,
    #             a_mn54 = sheet.cell(row=i, column=12).value
    #         )
    #         data.append(cassete)
    #     print(data)