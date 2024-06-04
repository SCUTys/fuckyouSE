# coding='utf-8'
import openpyxl
import unicodedata
from collections import OrderedDict
import pandas as pd

def remove_duplicates_and_emojis(df):
    print("开始处理原始文件: \n")

    new_df = pd.DataFrame(columns=df.columns)

    comments_dict = OrderedDict()

    for index, row in df.iterrows():
        content = row['content']
        if not content:
            continue

        content_no_emoji = remove_emojis(content)
        if content_no_emoji not in comments_dict:
            comments_dict[content_no_emoji] = row

    for index, row in enumerate(comments_dict.values(), start=1):
        row['content'] = remove_emojis(row['content'])
        new_df.loc[index] = row

    print("数据清理完毕，表情已删除。")

    return new_df

def remove_emojis(text):
    """
    移除文本中的表情符号

    参数:
    - text (str): 输入文本

    返回:
    - str: 去除表情符号后的文本
    """
    clean_text = ""
    for char in text:
        if unicodedata.category(char) != 'So':
            clean_text += char
    return clean_text


remove_duplicates_and_emojis('output/original_data.xlsx', 'output/cleaned_data.xlsx')
