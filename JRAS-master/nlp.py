# coding='utf-8'
import matplotlib.pyplot as plt
from snownlp import SnowNLP
import pandas as pd

def sentiment_analysis(df):
    """
    情感分析

    步骤：
    """

    # 1. 对读取的每一行文本进行情感分析，并将结果存入sentimentslist列表
    sentimentslist = []
    for index, row in df.iterrows():
        s = SnowNLP(row['content'])
        sentimentslist.append(s.sentiments)

    # 2. 统计情感得分中积极和消极的数量
    positive = len([s for s in sentimentslist if s >= 0.5])
    negative = len([s for s in sentimentslist if s < 0.5])

    # 3. 定义饼图的标签、大小及颜色
    labels = ['Positive', 'Negative']
    sizes = [positive, negative]
    colors = ['green', 'red']

    # 4. 绘制饼图并设置样式
    plt.pie(sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%')
    plt.title('Analysis of Sentiments')
    plt.savefig("output/sentiment_analysis_pie_chart.png",
                dpi=300,
                bbox_inches='tight')
