'''from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Registration, name='Registration'),
]
'''
from django.urls import path
from login.views import PersonListView, PersonCreateView, PersonUpdateView

urlpatterns = [
    path(''.https://www.pexels.com/photo/landscape-sky-clouds-hd-wallpaper-55787/, name = 'sky_image'),
    path('', PersonListView.as_view(), name='person_list'),
    path('add/', PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/edit/', PersonUpdateView.as_view(), name='person_edit'),
]
