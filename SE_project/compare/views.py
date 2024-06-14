import json
import sqlite3

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def compare_mainwindow(request):
    context = {}
    #读取数据库
    conn = sqlite3.connect('jd_comments.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT product_id from compare")
    phone_ids = cursor.fetchall()
    infos=[]
    for phone_id in phone_ids:
        cursor.execute(f"SELECT brief FROM product WHERE product_id = {phone_id[0]}")
        phone_info = cursor.fetchone()[0]
        cursor.execute(f"SELECT detail FROM product WHERE product_id = {phone_id[0]}")
        phone_detail = cursor.fetchone()[0]
        phone_info = json.loads(phone_info)
        phone_detail = json.loads(phone_detail)
        infos.append({
            'phone_id': phone_id[0],
            'phone_name': phone_info['name'],
            'phone_price': phone_info['price'],
            'phone_img': phone_info['image'],
            'details': phone_detail,
        })
    conn.close()
    context['infos'] = infos
    return render(request, 'compare.html', context)

def delete_compare(request):
    phone_id = request.POST.get("phone_id")
    print(phone_id)
    conn = sqlite3.connect('jd_comments.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM compare WHERE product_id = {phone_id}")
        conn.commit()
        conn.close()
        return JsonResponse({"status":True})
    except Exception as e:
        print(e)
        conn.close()
        return JsonResponse({"status":False})

    # namelist=["华为Mate60"]
    # prices=["9999"]
    # screenSizes=["aaa"]
    # screenResolutions=[""]
    # refreshrates=[""]
    # memorys=[""]
    # storages=[""]
    # cameraFronts=[""]
    # cameraBacks=[""]
    # batteryCapacitys=[""]
    # chargingPowers=[""]
    # chargingPowerWirelesss=[""]
    # cpus=[""]
    # operatingSyss=[""]
    # availabilitys=[""]
    # colors=[""]
    # positiveRates=[""]
    # saless=[""]
    # context={
    # "namelist":namelist,
    # "prices":prices,
    # "screenSizes" :screenSizes,
    # "screenResolutions":screenResolutions,
    # "refreshrates":refreshrates,
    # "memorys" :memorys,
    # "storages":storages,
    # "cameraFronts" :cameraFronts,
    # "cameraBacks":cameraBacks,
    # "batteryCapacitys" :batteryCapacitys,
    # "chargingPowers" :chargingPowers,
    # "chargingPowerWirelesss" :chargingPowerWirelesss,
    # "cpus":cpus,
    # "operatingSyss" :operatingSyss,
    # "availabilitys" :availabilitys,
    # "colors" :colors,
    # "positiveRates":positiveRates,
    # "saless" :saless,
    # }
    # return render(request, 'compare.html',context)
# def compare_list(request):
#     compares = CompareModel.objects.all()
#     table = CompareTable(compares)
#     return render(request, 'compare.html', {'table': table})