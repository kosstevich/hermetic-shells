from dataclasses import dataclass
from openpyxl import load_workbook
from datetime import datetime
import statistics

@dataclass
class Shell:
    id: int             # Row number in the table
    a_i131: float       # Activity I^131
    a_cs134: float 
    a_cs136: float 
    a_cs137: float 
    a_mn54: float
    status: int         # 0 - hermetic, 1 - not hermetic, 2 - unknown

    def to_list(self)->list: return [self.id, self.a_cs134, self.a_cs136, self.a_cs137, self.a_mn54]

@dataclass
class Cassete(Shell):           
    id1: int            # Measure number
    id2: int            # Id cassete
    name: str           # Cassete name
    coordinates: str    # Cassete coordinates
    date_time: datetime  
    companies: int      # Cassete age
    id_pen: int         # Number of experemental penal

    def to_Shell(self)->Shell:
        cassete_data = Shell(
            id = self.id,
            a_i131 = self.a_i131,
            a_cs134=self.a_cs134,
            a_cs136=self.a_cs136,
            a_cs137=self.a_cs134,
            a_mn54=self.a_mn54
        )
        return cassete_data

    def to_list(self)->list: return [self.id, self.id1, self.id2, self.name, self.coordinates, 
                                self.date_time, self.companies, self.id_pen, self.a_cs134, self.a_cs136, self.a_cs137, self.a_mn54]

class Data:
    def __init__(self, filename:str = "data/sample-data.xlsx", sheet_name:str = "Лист1"):
        self.input_data, self.cass_indexes = self._read(filename, sheet_name)

    def _read(self, filename:str, sheet_name:str):
        file = load_workbook(filename)
        sheet = file.get_sheet_by_name(sheet_name)
        rows = sheet.max_row
        input = []
        indexes = []

        for i in range(2, rows + 1):
            if sheet.cell(row=i, column=6).value == None:
                break
            cassete = Cassete(
                id = i,
                id1 = sheet.cell(row=i, column=1).value,
                id2 = sheet.cell(row=i, column=2).value,
                name = sheet.cell(row=i, column=3).value,
                coordinates = sheet.cell(row=i, column=5).value,
                date_time = sheet.cell(row=i, column=6).value,
                companies = sheet.cell(row=i, column=7).value,
                id_pen = sheet.cell(row=i, column=8).value,
                a_i131 = sheet.cell(row=i, column=9).value,
                a_cs134 = sheet.cell(row=i, column=10).value,
                a_cs136 = sheet.cell(row=i, column=13).value,
                a_cs137 = sheet.cell(row=i, column=11).value,
                a_mn54 = sheet.cell(row=i, column=12).value
            )
            input.append(cassete)
            indexes.append(i)
        return input, indexes
    
    def _get_list_by_range_id(self, left:int, right:int)->list:
        output = []
        for i in range(left, right+1): output.append(self.input_data[self.cass_indexes.index(i)])
        return output
    
    def divide_into_intervals(self, intervals:list)->list: 
        intervals_data = [[]]
        #TODO
        return intervals_data

class Fragment:
    def __init__(self, fragment:list):
        self.data = []
        for i in range(0,len(fragment)):
            data.append(fragment.to_Shell)

    def calc_fields(self):
        #TODO
        # self.a_i131_amean = statistics.mean(self.data.)     # Arithmetic mean activity I^131
        pass