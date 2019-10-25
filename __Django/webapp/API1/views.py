from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json


# Create your views here.

@api_view (['POST'])

def IdealWeight(heightdata):
    try:
        height = json.loads(heightdata.body)
        #height = str(height)
        #height = json.loads(heightdata)
        weight = str(height*10)
        #return JsonResponse(height, 'API1/api1.html', safe=False)
        #return render(height, 'API1/api1.html')
        return JsonResponse('Ideal weight should be: ' + weight + 'Kg', safe=False)
    except ValueError as e:
        return Response(e.arg[0], status.HTTP_400_BAD_REQUEST)
    except:
        print('An exception occurred')

