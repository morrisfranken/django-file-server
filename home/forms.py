'''
Created on 10 Sep 2018

@author: morris
'''
from django import forms
from .models import Uploads


class UploadForm(forms.ModelForm):
    overwrite = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Uploads
        fields = ('file', 'is_private', 'overwrite')
        widgets = {
            'file': forms.FileInput(attrs={'multiple' : True, 'class' : 'hidden'})
        }
        labels = {
            "is_private": "Private (requires login to download)",
        }