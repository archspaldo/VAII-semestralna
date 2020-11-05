from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from .models import Discussion
from django.views.generic import ListView

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


class IndexView(ListView):
    model = Discussion
    paginate_by = 10
    context_object_name = 'discussion'
    template_name = 'app/index.html'


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/confirmation.html', get_context('login'))
        else:
            return render(request, 'app/login.html', get_context('login'))


def user_login(request):
    logout(request)
    if request.POST:
        user = authenticate(
            username=request.POST['meno'], password=request.POST['heslo'])
        if user is not None:
            login(request, user)
            set_context('login', {'message': 'Uspešné prihlásenie', })
            return HttpResponseRedirect(reverse('app:login'))
    set_context('login', {'error': 'Meno alebo heslo sú nesprávne', })
    return HttpResponseRedirect(reverse('app:login'))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:login'))
