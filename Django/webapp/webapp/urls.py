"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path
# from django.conf.urls import include, url
# from login.views import

urlpatterns = [
    # path('', include('login.urls')),
    # path('admin/', admin.site.urls),
    # url(r'^login/', include('login.urls')),
    # url(r'^API1/', include('API1.urls')),
    # path('', PersonListView.as_view(), name='person_list'),
    # path('add/', PersonCreateView.as_view(), name='person_add'),
    # path('<int:pk>/edit/', PersonUpdateView.as_view(), name='person_edit'),
]
'''
from django.urls import path

from login.views import PersonListView, PersonCreateView, PersonUpdateView

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
    path('add/', PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/edit/', PersonUpdateView.as_view(), name='person_edit'),
]'''
