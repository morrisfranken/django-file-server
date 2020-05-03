'''
Created on 4 Apr 2016

@author: morris
'''
from django.conf.urls import url

from . import views

app_name = "users"

urlpatterns = [
    url(r'^create/?$', views.create, name='create'),
    url(r'^login/?$', views.login, name="login"),
    url(r'^logout/?$', views.logout, name="logout"),
]