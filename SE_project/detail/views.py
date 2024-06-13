import base64
import sqlite3
from threading import Thread

import imageio
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.http import FileResponse
import os

from JRAS import  spider
from detail.mytools.Converter import JsonToTxtConverter
from django.urls import reverse

json2text = JsonToTxtConverter()
from detail.WordCloudMaster import create_word_cloud as CWC

# PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


class WC_WorkerThread(Thread):
    def __init__(self,product_id):
        super().__init__()
        self.product_id=product_id
    def run(self):
        comment=spider.spider_comment(self.product_id)
        conn = sqlite3.connect('jd_comments.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE product SET comment ='{comment}' WHERE product_id = {self.product_id}")
        conn.commit()
        conn.close()





def generate_word_cloud(comments, image_path):
    #根据字符串生成词云
    # comments = comments
    # image_path = image_path
    cloud_image_path = CWC.create_wordscloud(comments, image_path)
    return cloud_image_path




from JRAS import spider
# Create your views here.
def detail_window(request, phone_id):
    # phone_id = phone_id
    # print("get phone id in detail_window",phone_id)
    # page_num = 1
    # comment=spider.spider_comment(phone_id,page_num)
    # print("comment",comment)
    # cloud_img=
    # phone_info=spider.spider_product(phone_id)[phone_id]
    conn = sqlite3.connect('jd_comments.sqlite3')
    cursor = conn.cursor()

    cursor.execute(f"SELECT brief FROM product WHERE product_id = {phone_id}")
    phone_info = cursor.fetchone()[0]
    cursor.execute(f"SELECT detail FROM product WHERE product_id = {phone_id}")
    phone_detail = cursor.fetchone()[0]

    conn.close()
    phone_info=json.loads(phone_info)
    phone_detail=json.loads(phone_detail)
    context={
        'phone_id':phone_id,
        'phone_name':phone_info['name'],
        'phone_price':phone_info['price'],
        'phone_img':phone_info['image'],
        'details':phone_detail,
    }


    return render(request,"detail.html",context)
import json
def generate_WC0(request):
    context={}
    if request.method == "POST":
        phone_id = request.POST.get("phone_id")
        print("get phone id in detail_window", phone_id)
        page_num = 1

        conn = sqlite3.connect('jd_comments.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"SELECT comment FROM product WHERE product_id = {phone_id}")
        comment = cursor.fetchone()[0]
        conn.close()

        print("comment", comment)
        # 执行Django逻辑
        folder_path = os.getcwd()
        # json_path=os.path.join(folder_path, "detail\\words\\test.json")
        image_path=os.path.join(folder_path, "detail\\wordcloud_img\\love.png")
        # wc_workerThread=WC_WorkerThread(comment,image_path)
        # wc_workerThread.run()
        # wc_path=wc_workerThread.get_wcpath()
        # result_img=open(wc_path, "rb").read()
        wc_path=generate_word_cloud(comment, image_path)
        result_img = open(wc_path, "rb").read()
        print("result_img")
        #将图片转成json
        encoded_img = base64.b64encode(result_img).decode()
        context={
            'result_img':encoded_img
        }

        return JsonResponse(context)
    else:
        return JsonResponse(context)
from JRAS import process

def check_comment(request):
    if request.method == "POST":
        phone_id = request.POST.get("phone_id")
        conn = sqlite3.connect('jd_comments.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"SELECT comment FROM product WHERE product_id = {phone_id}")
        comment = cursor.fetchone()[0]
        conn.close()
        if comment!="":
            return JsonResponse({ 'has_comment': True})
        else:
            return JsonResponse({ 'has_comment': False})
    else:
        return JsonResponse()


def generate_WC(request):
    context={}
    if request.method == "POST":
        phone_id = request.POST.get("phone_id")
        print("get phone id in detail_window", phone_id)
        page_num = 1

        conn = sqlite3.connect('jd_comments.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"SELECT comment FROM product WHERE product_id = {phone_id}")
        comment = cursor.fetchone()[0]
        conn.close()


        wc_path_p,wc_path_n = process.chinese_word_segmentation(comment)
        result_img_p = open(wc_path_p, "rb").read()
        result_img_n = open(wc_path_n, "rb").read()
        print("result_img")
        # 将图片转成json
        encoded_img_p = base64.b64encode(result_img_p).decode()
        encoded_img_n = base64.b64encode(result_img_n).decode()
        context = {
            'result_img_p': encoded_img_p,
            'result_img_n': encoded_img_n
        }
        return JsonResponse(context)
    else:
        return JsonResponse(context)



def call_detail(request):
    context = {}
    phone_id = ""
    if request.method == 'POST':
        # 获取POST数据
        post_data = request.POST
        phone_id = post_data.get("phone_id")
        print("get phone_id", phone_id)
    context = {
        'phone_id': phone_id
    }



    ##将keyword储存到数据库中
    # print("keyword",keyword)
    print("context in call", context)
    url = reverse("detail_phone_id", args=[phone_id])
    return redirect(url)
    # return  render(request, "detail.html", context)