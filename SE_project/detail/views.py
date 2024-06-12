

import imageio
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.http import FileResponse
import os


from detail.mytools.Converter import JsonToTxtConverter
from django.urls import reverse

json2text = JsonToTxtConverter()
from detail.WordCloudMaster import create_word_cloud as CWC

# PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


class WC_WorkerThread():
    def __init__(self, json_path, image_path):
        super().__init__()
        self.json_path = json_path
        self.image_path = image_path
        self.cloud_image_path=""
    def run(self):
        txt_path = json2text.convert_to_txt_file(self.json_path)
        print(txt_path, self.image_path)
        ##后续将文件存到数据库中
        self.cloud_image_path = CWC.create_wordscloud(txt_path, self.image_path)
        print('路径: ', txt_path, self.image_path, self.cloud_image_path, sep='\n')
        # bat_file_path = os.path.join(os.path.dirname(self.json_path), "generateWordCloud.bat")
        # subprocess.run([bat_file_path])
    def get_wcpath(self):
        return self.cloud_image_path

# Create your views here.
def detail_window(request, phone_id):
    phone_id = phone_id
    print("get phone id in detail_window",phone_id)
    print("waiting...")
    return render(request,"detail.html")
import json
def generate_WC(request):
    if request.method == "GET":
        # 执行Django逻辑
        folder_path = os.getcwd()
        json_path=os.path.join(folder_path, "detail\\words\\test.json")
        image_path=os.path.join(folder_path, "detail\\wordcloud_img\\love.png")
        wc_workerThread=WC_WorkerThread(json_path,image_path)
        wc_workerThread.run()
        wc_path=wc_workerThread.get_wcpath()
        result_img=open(wc_path, "rb").read()
        print("result_img")
        return HttpResponse(result_img, content_type='image/png')
    else:
        return render(request, "detail.html")

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
