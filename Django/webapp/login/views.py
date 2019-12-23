'''
from django.shortcuts import render
from .models import Register

# Create your views here.

def Registration(request):
    if request.method == 'POST':
        if request.POST.get('Username') and request.POST.get('Email') and request.POST.get('Password'):
            post = Register()
            post.Username = request.POST.get('Username')
            post.Email = request.POST.get('Email')
            post.Password = request.POST.get('Password')
            post.save()

            return render(request, 'base.html')

    else:
        return render(request, 'base.html')
'''

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from login.models import Register
from login.forms import PersonForm
from django.template import Template , Context


class PersonListView(ListView):
    model = Register
    context_object_name = 'Register'

class PersonCreateView(CreateView):
    model = Register
    fields = ('Username', 'Email', 'Password')
    success_url = reverse_lazy('person_list')

class PersonUpdateView(UpdateView):
    model = Register
    form_class = PersonForm
    template_name = 'people/person_update_form.html'
    success_url = reverse_lazy('person_list')
