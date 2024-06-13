import json
from time import sleep
from django.shortcuts import HttpResponse, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from JRAS import spider
import sqlite3
import threading

# from ajax.decorators import ajax
# Create your views here.
# @ajax
flag = False


def mycrawler(keyword):
    # keyword=request.POST.get('keyword')
    print("keyword")
    print(keyword)
    # 根据keyword爬虫
    cookie = "shshshfpa=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; shshshfpx=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; __jdu=17134908428041536521440; __jdv=76161171|www.bing.com|-|referral|-|1716431528090; pinId=gpXgCqz9ZronTwmVTfLR3g; pin=jd_hoCgxwDRQSiQ; unick=jd_es2lk4sv85zfx8; _tp=ezZG5SVF%2BP5fpYqKEfdi1Q%3D%3D; _pst=jd_hoCgxwDRQSiQ; qrsc=3; TrackID=1eTKDQOFnNxPQGaszQJ7torU2Qqbg4mvGoH5prNMNLNIm71TXDBqLjxi78yUCPyDwa0pDT8mChvTco3Xst3YSEWEgWQFoeFaWA-CmXkK0gFqOiJJHKXJa6DQFSW9yuNM8; thor=0154BEF7F3ABAD2AC9F8B853DF438E2DA2332B6EEBDE1EF9CABCA0BF63AC50772C4CE028EA18C2550B6EDD12A9510B9DB71B1A0EB13F0A7415C17FEAD235FF17DB3AC1D70F66C4FED351BC4E47D2FDC671664E42EAB6C140E1C8A7B1704898B5D433763206537128AC9359EA24D83CBBD8E0075E5E5208E30CE94F3D41DC9E047753B556FBF6D0CE2F46D9426B7250FE230EF6636AC5F02A70E2D946B2626A28; flash=2_3aLITYetDX6Zi8jYaqTco3DK5oucL4MKdqqXvSC8wGcIrOEq7T49XQ89zr-XdZ0V-g41NpdhIsDt0oi97TJPWi0fdbNyuW5lcLgFChRqLi5dQOgmg9O-BkLfVkSaa_iejQe0ApYr-ASEdTUFG_BWlG9U70B9qdmobGIWHYv-fFp*; areaId=19; ipLoc-djd=19-1601-0-0; 3AB9D23F7A4B3CSS=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; rkv=1.0; __jda=143920055.17134908428041536521440.1713490843.1717553599.1717640026.8; __jdc=143920055; shshshfpb=BApXclwtd6OpA6EGcp9UfDKqqq-EXN_UyBlEID21s9xJ1MiXwPIC2; 3AB9D23F7A4B3C9B=TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4; avif=1; __jdb=143920055.5.17134908428041536521440|8.1717640026"
    id_page_num = 1
    data_page_num = 1
    content = keyword
    # 获取爬取后得到的数据
    phone_ids = spider.spider_product(cookie, content, id_page_num)  # 手机名称

    conn = sqlite3.connect('jd_comments.sqlite3')
    cursor = conn.cursor()

    # print("get id!",phone_ids)
    # phone_ids=["111","222"]
    phone_datas = {}
    flag = True
    for phone_id in phone_ids:
        # form a new table to store comments for phone_id
        cursor.execute(f"CREATE TABLE IF NOT EXISTS phone_{phone_id} (username TEXT, id TEXT, content TEXT, creationTime TEXT)")
        phone_data = spider.spider_data(data_page_num, phone_id)
        for i in range(len(phone_data)):
            print(phone_data.loc[i]['nickname'], phone_data.loc[i]['id'], phone_data.loc[i]['内容'], phone_data.loc[i]['时间'])
            cursor.execute(
                f"INSERT INTO phone_{phone_id} (username, id, content, creationTime) VALUES ('{phone_data.loc[i]['nickname']}', '{phone_data.loc[i]['id']}', '{phone_data.loc[i]['内容']}', '{phone_data.loc[i]['时间']}')")
        conn.commit()
        phone_datas[phone_id] = phone_data

    if phone_ids == [] or phone_datas == {}:
        flag = False
    context = {
        "phone_ids": phone_ids,
        "phone_datas": phone_datas,
        'task_done': True,
        'status': flag
    }
    conn.close()
    return context
def mycrawler_brief(keyword):
    # keyword=request.POST.get('keyword')
    print("keyword")
    print(keyword)
    # 根据keyword爬虫
    cookie = "shshshfpa=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; shshshfpx=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; __jdu=17134908428041536521440; __jdv=76161171|www.bing.com|-|referral|-|1716431528090; pinId=gpXgCqz9ZronTwmVTfLR3g; pin=jd_hoCgxwDRQSiQ; unick=jd_es2lk4sv85zfx8; _tp=ezZG5SVF%2BP5fpYqKEfdi1Q%3D%3D; _pst=jd_hoCgxwDRQSiQ; qrsc=3; TrackID=1eTKDQOFnNxPQGaszQJ7torU2Qqbg4mvGoH5prNMNLNIm71TXDBqLjxi78yUCPyDwa0pDT8mChvTco3Xst3YSEWEgWQFoeFaWA-CmXkK0gFqOiJJHKXJa6DQFSW9yuNM8; thor=0154BEF7F3ABAD2AC9F8B853DF438E2DA2332B6EEBDE1EF9CABCA0BF63AC50772C4CE028EA18C2550B6EDD12A9510B9DB71B1A0EB13F0A7415C17FEAD235FF17DB3AC1D70F66C4FED351BC4E47D2FDC671664E42EAB6C140E1C8A7B1704898B5D433763206537128AC9359EA24D83CBBD8E0075E5E5208E30CE94F3D41DC9E047753B556FBF6D0CE2F46D9426B7250FE230EF6636AC5F02A70E2D946B2626A28; flash=2_3aLITYetDX6Zi8jYaqTco3DK5oucL4MKdqqXvSC8wGcIrOEq7T49XQ89zr-XdZ0V-g41NpdhIsDt0oi97TJPWi0fdbNyuW5lcLgFChRqLi5dQOgmg9O-BkLfVkSaa_iejQe0ApYr-ASEdTUFG_BWlG9U70B9qdmobGIWHYv-fFp*; areaId=19; ipLoc-djd=19-1601-0-0; 3AB9D23F7A4B3CSS=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; rkv=1.0; __jda=143920055.17134908428041536521440.1713490843.1717553599.1717640026.8; __jdc=143920055; shshshfpb=BApXclwtd6OpA6EGcp9UfDKqqq-EXN_UyBlEID21s9xJ1MiXwPIC2; 3AB9D23F7A4B3C9B=TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4; avif=1; __jdb=143920055.5.17134908428041536521440|8.1717640026"
    id_page_num = 1

    content = keyword
    # 获取爬取后得到的数据
    phone_infos = spider.spider_product(cookie, content)
    context={}
    flag = True
    if phone_infos == {}:
        flag = False
    context = {
        "phone_infos": phone_infos,
        'task_done': True,
        'status': flag
    }
    return context

def mycrawler_db(keyword):
    cookie = "shshshfpa=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; shshshfpx=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; __jdu=17134908428041536521440; __jdv=76161171|www.bing.com|-|referral|-|1716431528090; pinId=gpXgCqz9ZronTwmVTfLR3g; pin=jd_hoCgxwDRQSiQ; unick=jd_es2lk4sv85zfx8; _tp=ezZG5SVF%2BP5fpYqKEfdi1Q%3D%3D; _pst=jd_hoCgxwDRQSiQ; qrsc=3; TrackID=1eTKDQOFnNxPQGaszQJ7torU2Qqbg4mvGoH5prNMNLNIm71TXDBqLjxi78yUCPyDwa0pDT8mChvTco3Xst3YSEWEgWQFoeFaWA-CmXkK0gFqOiJJHKXJa6DQFSW9yuNM8; thor=0154BEF7F3ABAD2AC9F8B853DF438E2DA2332B6EEBDE1EF9CABCA0BF63AC50772C4CE028EA18C2550B6EDD12A9510B9DB71B1A0EB13F0A7415C17FEAD235FF17DB3AC1D70F66C4FED351BC4E47D2FDC671664E42EAB6C140E1C8A7B1704898B5D433763206537128AC9359EA24D83CBBD8E0075E5E5208E30CE94F3D41DC9E047753B556FBF6D0CE2F46D9426B7250FE230EF6636AC5F02A70E2D946B2626A28; flash=2_3aLITYetDX6Zi8jYaqTco3DK5oucL4MKdqqXvSC8wGcIrOEq7T49XQ89zr-XdZ0V-g41NpdhIsDt0oi97TJPWi0fdbNyuW5lcLgFChRqLi5dQOgmg9O-BkLfVkSaa_iejQe0ApYr-ASEdTUFG_BWlG9U70B9qdmobGIWHYv-fFp*; areaId=19; ipLoc-djd=19-1601-0-0; 3AB9D23F7A4B3CSS=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; rkv=1.0; __jda=143920055.17134908428041536521440.1713490843.1717553599.1717640026.8; __jdc=143920055; shshshfpb=BApXclwtd6OpA6EGcp9UfDKqqq-EXN_UyBlEID21s9xJ1MiXwPIC2; 3AB9D23F7A4B3C9B=TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4; avif=1; __jdb=143920055.5.17134908428041536521440|8.1717640026"
    page_num = 1
    data={}
    content = keyword
    # 获取爬取后得到的数据
    product_infos=spider.spider(cookie,keyword, page_num)

    # conn = sqlite3.connect('jd_comments.sqlite3')
    # cursor = conn.cursor()
    #
    #
    # # 执行SQL查询
    # cursor.execute("SELECT product_id, brief FROM product WHERE brief IS NOT NULL")
    #
    # # 获取所有行
    # rows = cursor.fetchall()
    # 将行转换为字典

    data=product_infos
    print(data)

    flag=True
    if data == {}:
        flag = False
    # 关闭数据库连接
    context = {
        "phone_infos": data,
        'task_done': True,
        'status': flag
    }
    return context






def check_task(request):
    keyword = request.POST.get('keyword')
    print("data", keyword)
    data = mycrawler_db(keyword)
    if data['status']:
        print("task success")

        context = {
            'phone_infos': data['phone_infos'],
            'task_done': data['task_done'],
            'status': data['status']
        }
        # print(context)
        return JsonResponse(context)
    else:

        context = {
            'phone_infos': [],
            'task_done': [],
            'status': data['status']
        }
        return JsonResponse(context)


# def waiting_page(request):
#     return render(request, 'waiting.html')
def searchresult_window(request, keyword):
    return render(request, 'searchresult.html', {"keyword": keyword})


def call_searchresult(request):
    context = {}
    keyword = ""
    if request.method == 'POST':
        # 获取POST数据
        post_data = request.POST
        keyword = post_data.get("keyword")
        print("get keyword", keyword)
    context = {
        'keyword': keyword
    }
    ##将keyword储存到数据库中

    # print("keyword",keyword)
    print("context in call", context)
    url = reverse("searchresult_keyword", args=[keyword])
    return redirect(url)

