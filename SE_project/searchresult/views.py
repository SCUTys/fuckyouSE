from django.shortcuts import render
from JRAS import spider
# Create your views here.
def searchresult_window(request):
    if request.method == 'POST':
        # 获取POST数据
        post_data = request.POST

        keyword= post_data.get("keyword")
        print("keyword")
        print(keyword)
        # 根据keyword爬虫


        #获取爬取后得到的数据
        phone_names=[]#手机名称
        context = {
            "phone_names": phone_names,
        }
        # ...



    return render(request,"searchresult.html",context)