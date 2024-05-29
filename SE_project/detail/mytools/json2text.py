import json
import os

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
        print(f'Successfully converted {self.json_file_path} to {self.txt_file_path}')
        return self.txt_file_path

