import json
import os
import xlrd
import openpyxl
import re

class XlsxToTxtConverter:
    def __init__(self):
        self.xlsx_file_path = None
        self.data = None
        self.txt_file_path = None
        self.file_type = None

    def convert_to_txt_file(self, file_path):
        self.xlsx_file_path = file_path
        self.txt_file_path = os.path.splitext(file_path)[0] + '.txt'
        self.file_type = os.path.splitext(file_path)[1].lower()

        if self.file_type == '.xls':
            workbook = xlrd.open_workbook(self.xlsx_file_path)
            sheet = workbook.sheet_by_index(0)
            self.data = [str(cell.value) for row in range(sheet.nrows) for cell in sheet.row(row)]
        elif self.file_type == '.xlsx':
            workbook = openpyxl.load_workbook(self.xlsx_file_path, data_only=True)
            sheet = workbook.active
            self.data = [str(cell.value) for row in sheet.iter_rows() for cell in row]
        else:
            raise ValueError('不支持的类型: {}'.format(self.file_type))

        # 去除head
        self.data = self.data[1:]
        # 去除空行
        self.data = [text for text in self.data if text.strip() != '']
        # 去除html标签
        self.data = [self.remove_html_tags(text) for text in self.data]

        with open(self.txt_file_path, 'w', encoding='utf-8') as f:
            f.writelines([sentence + '\n' for sentence in self.data])

        print(f'转换成功:  {self.xlsx_file_path} to {self.txt_file_path}')
        return self.txt_file_path

    def remove_html_tags(self, text):
        # 去除html标签
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)




class JsonToTxtConverter:
    def __init__(self):
        self.json_file_path = None
        self.data = None
        self.txt_file_path = None

    def convert_to_txt_file(self, json_file_path):
        self.json_file_path = json_file_path
        self.txt_file_path = os.path.splitext(json_file_path)[0] + '.txt'
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        with open(self.txt_file_path, 'w', encoding='utf-8') as f:
            for item in self.data:
                for sentence in item['text']:
                    f.write(sentence + '\n')
        print(f'转换成功:  {self.json_file_path} to {self.txt_file_path}')
        return self.txt_file_path


def test():
    xlsx = XlsxToTxtConverter()
    txtpath = xlsx.convert_to_txt_file('../resource/线上学习-关系2_1678766818257.xls')
    print(txtpath)

# test()