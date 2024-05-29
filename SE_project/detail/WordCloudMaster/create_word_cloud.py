import jieba
import codecs
import sys
import pandas
import numpy as np
from wordcloud import WordCloud
import imageio
from wordcloud import WordCloud, ImageColorGenerator
import os
from os import listdir
from os.path import isfile, join
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))

#停止词文件目录
stopwords_filename = os.path.join(main_path,'WordCloudMaster','data','stopwords.txt')
#字体文件目录
font_filename = os.path.join(main_path,'WordCloudMaster','fonts','STFangSong.ttf')

#词云背景颜色
word_background_color='white'
#字体最大大小
word_size=600

#分词过滤函数
def cut(input_filename):
    content = '\n'.join([line.strip()
                         for line in codecs.open(input_filename, 'r', 'utf-8')
                         if len(line.strip()) > 0])
    stopwords = set([line.strip()
                     for line in codecs.open(stopwords_filename, 'r', 'utf-8')])

    segs = jieba.cut(content)
    words = []
    for seg in segs:
        word = seg.strip().lower()
        if len(word) > 1 and word not in stopwords:
            words.append(word)
    return words

#词语出现次数统计函数
def word_counting(words):
    
    #创建由分词过滤后的词语表格words_df。
    words_df = pandas.DataFrame({'word': words})
    #统计词语出现的次数
    words_stat = words_df.groupby(by=['word'])['word'].agg(np.size)
    words_stat = words_stat.to_frame()
    #按词语出现的次数重排表格
    words_stat.columns = ['number']
    words_stat = words_stat.reset_index().sort_values(by="number", ascending=False)
    return words_stat

#生成词云函数
def create_wordscloud(input_filename,background_picture_filename):    
    words=cut(input_filename)
    words_stat=word_counting(words)
    print('# of different words =', len(words_stat))       
    input_prefix = '.'.join(input_filename[-6:-5])   
    if background_picture_filename[-4:] != '.png' and background_picture_filename[-4:] != '.jpg':
        print('# of different words =', len(words_stat))
        return 0
    
    if isfile(background_picture_filename):        
        bimg = imageio.imread(background_picture_filename)
        wordcloud = WordCloud(font_path=font_filename, background_color=word_background_color,
                                mask=bimg, max_font_size=word_size, random_state=100)
        wordcloud = wordcloud.fit_words(
            dict(words_stat.head(100).itertuples(index=False)))

        bimgColors = ImageColorGenerator(bimg)
        wordcloud.recolor(color_func=bimgColors)

        # output_filename = prefix + '_' + input_prefix + '.png'
        filepath, _ = os.path.splitext(input_filename)
        pic_name, _ = os.path.splitext(os.path.basename(background_picture_filename))
        # output_filename = os.path.join(main_path,'resource',input_prefix+'_cloud.png')
        output_filename = filepath + '_' + pic_name + '_cloud.png'
        print('Saving', output_filename)
        wordcloud.to_file(output_filename)
        return output_filename



if __name__ == '__main__':
    print(font_filename)
    def aaa():
        main_path = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
        text_path = os.path.join(main_path, 'words', 'test.txt')
        pic_path = os.path.join(main_path, 'wordcloud_img', 'love.png')
        result_path = create_wordscloud(text_path, pic_path)
        print(result_path)
    aaa()
    pass
    
    # print(sys.argv)
    # if len(sys.argv) == 3:
    #     create_wordscloud(sys.argv[1],sys.argv[2])
    # # if len(sys.argv) == 2:
    # #     create_wordscloud(sys.argv[0],sys.argv[1])
    # else:
    #     print('[usage] <input>')
