from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'app/index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'app/login.html')
