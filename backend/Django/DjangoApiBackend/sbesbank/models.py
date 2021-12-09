from django.db import models
from django.db.models.fields import DateField

# Create your models here.

class IUser(models.Model):
    fullName = models.CharField(max_length = 50, unique = False)
    password = models.CharField(max_length = 100)
    username = models.CharField(max_length = 40, unique = True)
    billingAddress = models.CharField(max_length = 50 )
    genders = {('female'), ('male')}
    gender = models.CharField(choices = genders)
    jmbg = models.BigIntegerField(unique = True)
    birthDate  = models.DateField()
    userTypes = {('admin'),('client')}
    userType = models.CharField(choices = userTypes)

class Client(models.Model):
    userId = models.ForeignKey(IUser, on_delete = models.CASCADE, unique = True)

class Certificate(models.Model):
    userId = models.ForeignKey(IUser, on_delete = models.CASCADE, unique = True)
    authorityName = models.CharField(max_length = 50)
    cerPath = models.CharField(max_length = 200, unique = True)
    pxfPath = models.CharField(max_length = 200, unique = True)
    pvkPath = models.CharField(max_length = 200, unique = True)
    certificateName = models.CharField(max_length = 100, unique = True)

