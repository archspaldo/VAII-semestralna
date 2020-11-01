from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, request


class IndexView(View):
    def get(self, request):
        return render(request, 'app/index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'app/login.html')


def user_login(request):
    logout(request)
    meno = ''
    heslo = ''
    if request.POST:
        pouzivatel = authenticate(
            username=request.POST['meno'], password=request.POST['heslo'])
        if pouzivatel is not None and pouzivatel.is_active:
            login(request, pouzivatel)
            return HttpResponseRedirect('app/index.html')
    return render(request, 'app/login.html', {'error': 'Meno alebo heslo sú nesprávne'})
