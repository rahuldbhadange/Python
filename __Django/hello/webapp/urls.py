from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Registration, name='Registration'),

    #url(r'^(?p<MovieName_id>[0-9]+)/$', views.details),
]