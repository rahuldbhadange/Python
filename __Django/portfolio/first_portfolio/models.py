from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True, unique=True)
    job_title = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    relationship_status = models.CharField(max_length=10, blank=True)
