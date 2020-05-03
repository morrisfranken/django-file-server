'''
Created on 4 Apr 2016

@author: morris
'''
from django.urls import path
from . import views

app_name = "download"

urlpatterns = [
    path('delete/<int:file_id>', views.delete_file),  # this has to be last, as it matches everything
    path('set_private/<int:file_id>', views.set_private),  # this has to be last, as it matches everything
    path('', views.home, name="home"),
]