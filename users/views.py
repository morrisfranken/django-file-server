# -*- coding: future_fstrings -*-
import ujson as json
import traceback
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from . import forms
from file_server import secrets


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                # print("logging using {}  ::  {} ".format(email, password))
                user = auth.authenticate(request, email=email, password=password)
                auth.login(request, user)
                print(f"{email} logged in")
                return HttpResponseRedirect('/')
            except:
                return HttpResponse("Ivalid login details", "status", status=401)
        else:
            return HttpResponse("Ivalid input", "status", status=401)

    print("showing login page")
    form = forms.UserLoginForm()
    invitation_code = request.GET.get('invitation_code')
    return render(request, 'login.html', {'form': form, 'invitation_code' : f"?invitation_code={invitation_code}" if invitation_code else ""})


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/users/login')


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('invitation_code') != secrets.INVITATION_CODE:
                return HttpResponse('Invalid Invitation code, please request your administrator for an invitation code', status=401)

            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                return HttpResponse('Passwords must match', status=401)

            try:
                User = get_user_model()
                user = User.objects.create_user(email=email, password=password1)
                auth.login(request, user)
                return HttpResponseRedirect('/')
            except Exception as e:
                print(traceback.format_exc())
                return HttpResponse('Email already in use', status=401)
    else:
        form = forms.UserRegisterForm(initial={'invitation_code' : request.GET.get('invitation_code')})
        return render(request, 'register.html', {'form': form})

