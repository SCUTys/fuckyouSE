from django.db import models

# Create your models here.
from django.db import models

class CompareModel(models.Model):
    names = models.CharField(max_length=100)
    prices = models.CharField(max_length=10)
    screenSizes = models.CharField(max_length=10)
    screenResolutions = models.CharField(max_length=10)
    refreshrates = models.CharField(max_length=10)
    memorys = models.CharField(max_length=10)
    storages = models.CharField(max_length=10)
    cameraFronts = models.CharField(max_length=10)
    cameraBacks = models.CharField(max_length=10)
    batteryCapacitys=models.CharField(max_length=10)
    chargingPowers=models.CharField(max_length=10)
    chargingPowerWirelesss=models.CharField(max_length=10)
    cpus=models.CharField(max_length=10)
    operatingSyss=models.CharField(max_length=10)
    availabilitys=models.CharField(max_length=10)
    colors=models.CharField(max_length=10)
    positiveRates=models.CharField(max_length=10)
    saless=models.CharField(max_length=10)
