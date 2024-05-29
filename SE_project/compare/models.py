from django.db import models

# Create your models here.
from django.db import models

class CompareModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    screenSize = models.CharField(max_length=10)
    screenResolution = models.CharField(max_length=10)
    refreshrate = models.CharField(max_length=10)
    memory = models.CharField(max_length=10)
    storage = models.CharField(max_length=10)
    cameraFront = models.CharField(max_length=10)
    cameraBack = models.CharField(max_length=10)
    batteryCapacity=models.CharField(max_length=10)
    chargingPower=models.CharField(max_length=10)
    chargingPowerWireless=models.CharField(max_length=10)
    cpu=models.CharField(max_length=10)
    operatingSys=models.CharField(max_length=10)
    availability=models.CharField(max_length=10)
    color=models.CharField(max_length=10)
    positiveRate=models.CharField(max_length=10)
    sales=models.CharField(max_length=10)
