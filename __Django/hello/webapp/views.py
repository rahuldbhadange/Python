from django.shortcuts import render
from .models import Register


def Registration(request):
    if request.method == 'POST':
        if request.POST.get('Username') and request.POST.get('Email') and request.POST.get('Password'):
            post = Register()
            post.Username = request.POST.get('Username')
            post.Email = request.POST.get('Email')
            post.Password = request.POST.get('Password')
            post.save()

            return render(request, 'webapp/Register.html')

    else:
        return render(request, 'webapp/Register.html')
