from django.shortcuts import render

# Create your views here.
def compare_mainwindow(request):
    namelist=["华为Mate60"]
    prices=["9999"]
    screenSizes=["aaa"]
    screenResolutions=[""]
    refreshrates=[""]
    memorys=[""]
    storages=[""]
    cameraFronts=[""]
    cameraBacks=[""]
    batteryCapacitys=[""]
    chargingPowers=[""]
    chargingPowerWirelesss=[""]
    cpus=[""]
    operatingSyss=[""]
    availabilitys=[""]
    colors=[""]
    positiveRates=[""]
    saless=[""]
    context={
    "namelist":namelist,
    "prices":prices,
    "screenSizes" :screenSizes,
    "screenResolutions":screenResolutions,
    "refreshrates":refreshrates,
    "memorys" :memorys,
    "storages":storages,
    "cameraFronts" :cameraFronts,
    "cameraBacks":cameraBacks,
    "batteryCapacitys" :batteryCapacitys,
    "chargingPowers" :chargingPowers,
    "chargingPowerWirelesss" :chargingPowerWirelesss,
    "cpus":cpus,
    "operatingSyss" :operatingSyss,
    "availabilitys" :availabilitys,
    "colors" :colors,
    "positiveRates":positiveRates,
    "saless" :saless,
    }
    return render(request, 'compare.html',context)
# def compare_list(request):
#     compares = CompareModel.objects.all()
#     table = CompareTable(compares)
#     return render(request, 'compare.html', {'table': table})