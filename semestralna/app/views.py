from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, request
from django.urls import reverse

context = {}


def get_context(key):
    global context
    value = context.get(key)
    if value or value == {}:
        context[key] = {}
    return value


def set_context(key, value):
    global context
    context[key] = value


class IndexView(View):
    def get(self, request):
        return render(request, 'app/index.html')


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/login_succ.html')
        else:
            return render(request, 'app/login.html', get_context('login'))


def user_login(request):
    logout(request)
    if request.POST:
        user = authenticate(
            username=request.POST['meno'], password=request.POST['heslo'])
        if pouzivatel is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('app:login'))
    set_context('login', {'error': 'Meno alebo heslo sú nesprávne', })
    return HttpResponseRedirect(reverse('app:login'))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:login'))
