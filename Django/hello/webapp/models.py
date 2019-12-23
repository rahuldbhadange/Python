from django.db import models

# Create your models here.

class Register(models.Model):
    Username= models.CharField(max_length=50, unique=True)
    Email= models.CharField(max_length=50, unique=True)
    Password= models.CharField(max_length=50)
