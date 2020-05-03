import ujson as json
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ipware.ip import get_ip

from . import forms

ip_white_list = ["195.114.237.186", "86.85.83.60", "127.0.0.1", ]

def create(request):
    # print(f"request from {get_ip(request)}")
    if not get_ip(request) in ip_white_list:
        return HttpResponse("Accounts may only be created at 3DUniversum")
    
    if request.method == 'POST':
        if request.POST.get("password") == request.POST.get("password2"):
            User = get_user_model()
            user = User.objects.create_user(email=request.POST.get("email"), password=request.POST.get("password"))
            return HttpResponse("Done! {}".format(user))
    form = forms.UserCreationForm()
    return render(request, 'create.html', {'form': form})


def login(request):
    if request.method == 'POST':
        print("checking form")
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                print("logging using {}  ::  {} ".format(email, password))
                user = auth.authenticate(request, email=email, password=password)
                auth.login(request, user)
                return HttpResponse("OK")
            except:
                return HttpResponse(json.dumps({"message" : "Ivalid login details", "status" : 401}, escape_forward_slashes=False), status=401, content_type='application/json')
        else:
            print("invalid form!")

    print("showing login page")
    form = forms.UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/users/login')


@login_required
def home(request):
    return render(request, 'home.html')

