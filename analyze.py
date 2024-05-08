from data import Data
from fragment import Fragment

class Analyze:
    def __init__(self):
        filename = input("Введите имя файла(data/sample-data.ods по умолчанию)")
        if filename == "":
            self.data = Data()
        else:
            self.data = Data(filename)

    def check_distribution(self):
        pass