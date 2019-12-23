from django.shortcuts import render, redirect, render_to_response
from django.http import request, response

# Create your views here.

def send(request):
    return render(request, "<h1><body> Sending Email</body></h1>")
