'''
Created on 10 Sep 2018

@author: morris
'''
from django import forms


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=255, required=True)
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), strip=False, required=True)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Validate password'}), strip=False, required=True)
    invitation_code = forms.CharField(label='Invitation code', widget=forms.TextInput(attrs={'placeholder': 'Invitation code'}), required=True)


class UserLoginForm(forms.Form):
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=255)
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), strip=False, )