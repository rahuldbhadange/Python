from django.contrib import admin
from . models import Person

# Register your models here.
admin.sites.register(Person)
