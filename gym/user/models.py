import datetime
import base64
from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=14)
    shelfNo = models.CharField(null=True, max_length=2)
    registerDate = models.DateField(auto_now=False)
    details = models.TextField(null=True)
    image = models.TextField(null=True)
    flag = models.BooleanField(default=False)


class Present(models.Model):
    date = models.DateField(auto_now=False)
    enterTime = models.TimeField()
    outTime = models.TimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Payment(models.Model):
    date = models.DateField(auto_now=False)
    price = models.IntegerField()
    method = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Exercise(models.Model):
    date = models.DateField(auto_now=False)
    details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)