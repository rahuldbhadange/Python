from django.db import models

# Create your models here.

class Register (models.Model):
    Username = models.CharField(max_length=50, unique=True, blank=True)
    Email = models.EmailField(max_length=50, unique=True, blank=True)
    Password = models.CharField(max_length=50)
