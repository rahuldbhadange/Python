'''from django.db import models

# Create your models here.

class Logon(models.Model):
    #print('Login here')
    logging_in = models.CharField(max_length=20,default='SOME STRING')

class Password(models.Model):
    #print('enter password')
    password_input = models.CharField(max_length=20)


'''