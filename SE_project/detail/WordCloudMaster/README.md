# wordcloud
wordcloud in python

# File System
- data
    - templates: users' pictures
    - stopwords.txt: stopwords which you do not want
- fonts: users' fonts

- create_word_cloud.py: main function
- preprocess.py: preprocess the QQ chat records

# Usage
First install `jieba` and `wordcloud`:
`pip3 install jieba`
and
`pip3 install wordcloud`

Then run code in terminal:
`python3 create_word_cloud.py filename.txt`

If you want to generate the wordcloud of QQ chat record, first preprocess the text file:
`python3 preprocess.py filename.txt`

Then run the main code:
`python3  create_word_cloud.py __filename.txt picture.txt`

For more details, read my blog post: [wordcloud](https://godweiyang.com/2019/07/27/wordcloud/)

生成词云功能模块：create_word_cloud.py
主要功能函数：create_wordscloud
使用方法：传入txt文件名和背景图片文件名（xxx.txt或xxx.png），函数中会自动加上前缀prefix组成相对路径，生成的词云图片保存在resource文件夹下，并返回词云文件保存的相对路径。