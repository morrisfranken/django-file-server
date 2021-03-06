'''
Created on 4 Apr 2016

@author: morris
'''
from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('uploads/', views.uploads),  # this has to be last, as it matches everything
    path('delete/<int:file_id>', views.delete_file),  # this has to be last, as it matches everything
    path('set_private/<int:file_id>', views.set_private),  # this has to be last, as it matches everything
    path('download/<path:download_path>', views.download),  # this has to be last, as it matches everything
    path('', views.home, name="home"),
]