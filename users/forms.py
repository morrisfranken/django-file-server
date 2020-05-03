'''
Created on 10 Sep 2018

@author: morris
'''
from django import forms


class UserCreationForm(forms.Form):
    email = forms.EmailField(
        label="email",
        max_length=255,
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        strip=False,
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(),
        strip=False,
    )


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="email",
        max_length=255,
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        strip=False,
    )