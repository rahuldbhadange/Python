from django.shortcuts import render
from . forms import Registration_Form

#from django.http import HttpResponse


# Create your views here.

def index1(request):
    form = Registration_Form()
    context = {
        'my_registration_form': form
    }
    return render(request,'login/index1111.html', context)
   # request render()
    #return HttpResponse (" <h1> login here </h1>")
