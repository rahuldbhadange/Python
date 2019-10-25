from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello World !!")


def year_archive(request):
    return HttpResponse("Year {}".format(request))
