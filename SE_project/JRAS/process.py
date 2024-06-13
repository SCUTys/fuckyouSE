# coding='utf-8'
import os

import openpyxl
import unicodedata
from collections import OrderedDict
import pandas as pd
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
#停止词文件目录
stopwords_filename = os.path.join(main_path,'JRAS','data','stopwords.txt')
bg_filename = os.path.join(main_path,'JRAS','data','bg.png')
out_filename_p = os.path.join(main_path,'JRAS','data','output_p.png')
out_filename_n = os.path.join(main_path,'JRAS','data','output_n.png')
# input:
#   comments:string
# return:
#   new_comments:list
def sentiment_analysis(comments):

    #去除无重复
    comments = remove_duplicates_and_emojis(comments)

    sentimentslist = []

    positive_comment, negative_comment = [], []

    middle_comment_number = 0

    for comment in comments:
        s = SnowNLP(comment)
        sentimentslist.append(s.sentiments)
        if s.sentiments < 0.4:
            negative_comment.append(comment)
        elif s.sentiments >= 0.6:
            positive_comment.append(comment)
        else:
            middle_comment_number += 1

    return positive_comment, negative_comment, [len(positive_comment), middle_comment_number, len(negative_comment)]

def remove_duplicates_and_emojis(comments):
    print("开始处理原始文件: \n")

    comments = comments.split('\n')

    comments_set = set()

    for comment in comments:
        if not comment:
            continue

        content_no_emoji = remove_emojis(comment)
        comments_set.add(content_no_emoji)

    new_comments = list(comments_set)

    return new_comments


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


# coding='utf-8'
import matplotlib.pyplot as plt
from snownlp import SnowNLP
import pandas as pd

#input:
#   comment:string
#return:
#   [positive_size, negative_size]
# def sentiment_analysis(comments):
#
#     #去除无重复
#     comments = remove_duplicates_and_emojis(comments)
#
#     sentimentslist = []
#
#     for comment in comments:
#         s = SnowNLP(comment)
#         sentimentslist.append(s.sentiments)
#
#     # 2. 统计情感得分中积极和消极的数量
#     positive = len([s for s in sentimentslist if s >= 0.5])
#     negative = len([s for s in sentimentslist if s < 0.5])
#
#     return [positive, negative]


# coding='utf-8'
import jieba
import jieba.analyse
import numpy as np
from PIL import Image
from openpyxl import load_workbook
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

def chinese_word_segmentation_help(comments,flag=0):
    """
    分词并生成词云

    参数:
    - df (dataframe): 之前清理过的数据

    步骤：
    1. 从df中提取评论内容进行分词
    2. 过滤停用词并保存分词结果到文本文件
    3. 统计分词结果的词频
    4. 使用背景图片和词频数据生成词云
    5. 保存词云图片
    """

    #去除无重复
    # comments = remove_duplicates_and_emojis(comments)

    # 设置停用词
    jieba.analyse.set_stop_words(stopwords_filename)
    stop_words = set()
    with open(stopwords_filename, 'r', encoding='utf-8') as f:
        for word in f:
            stop_words.add(word.strip())

    # 从comment中提取评论内容并分词
    segmented_words = []
    for comment in comments:
        if comment is not None:
            words = jieba.cut(comment)
            words_filtered = ' '.join(word for word in words if word not in stop_words)
            segmented_words.append(words_filtered)

    # 统计词频
    word_freq = {}
    for words in segmented_words:
        for word in words.split():
            if word not in stop_words:
                if word not in word_freq:
                    word_freq[word] = 0
                word_freq[word] += 1

    # 加载背景图片并生成词云
    img = Image.open(bg_filename)
    mask = np.array(img)

    wordcloud = WordCloud(width=1000, height=1000, mask=mask, background_color='white', font_path='STKAITI.TTF',
                          stopwords=stop_words, random_state=50, max_words=40)
    wordcloud.generate_from_frequencies(word_freq)

    # # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')

    if flag==0:
        wordcloud.to_file(out_filename_p)
    else:
        wordcloud.to_file(out_filename_n)

def chinese_word_segmentation(comments):
    comments_p,comments_n,_=sentiment_analysis(comments)

    chinese_word_segmentation_help(comments_p, 0)
    chinese_word_segmentation_help(comments_n, 1)
    return out_filename_p,out_filename_n
