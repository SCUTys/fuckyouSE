import json
import os
import openpyxl

class XlsxToTxtConverter:
    def __init__(self):
        self.xlsx_file_path = None
        self.data = None
        self.txt_file_path = None

    def convert_to_txt_file(self, xlsx_file_path):
        self.xlsx_file_path = xlsx_file_path
        self.txt_file_path = os.path.splitext(xlsx_file_path)[0] + '.txt'
        workbook = openpyxl.load_workbook(self.xlsx_file_path, data_only=True)
        sheet = workbook.active
        self.data = [str(cell.value) for row in sheet.iter_rows() for cell in row]
        with open(self.txt_file_path, 'w', encoding='utf-8') as f:
            f.writelines([sentence + '\n' for sentence in self.data])
        print(f'Successfully converted {self.xlsx_file_path} to {self.txt_file_path}')
        return self.txt_file_path
