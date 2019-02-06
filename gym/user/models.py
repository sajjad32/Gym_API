import datetime

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=12)
    shelfNo = models.CharField(max_length=2)
    details = models.TextField()
    flag = models.BooleanField(default=False)

class Present(models.Model):
    date = models.DateField(auto_now=False)
    enterTime = models.TimeField()
    outTime = models.TimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Payment(models.Model):
    date = models.DateField()
    price = models.IntegerField()
    method = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
