'''
Created on 4 Apr 2016

@author: morris
'''
from django.urls import path
from . import views

app_name = "download"

urlpatterns = [
    # path('videos/<uuid:video_id>/video.<path:ext>', views.download_video),
    path('<path:download_path>', views.download),  # this has to be last, as it matches everything
]