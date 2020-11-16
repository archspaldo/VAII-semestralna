from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from .models import Discussion
from django.views.generic import ListView
from .forms import DiscussionForm
import datetime


class IndexView(ListView):
    model = Discussion
    paginate_by = 1
    context_object_name = 'discussion'
    template_name = 'app/index.html'


class TestView(View):
    def get(self, request):
        return render(request, 'app/test.html')


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/logged_in.html')
        else:
            return render(request, 'app/login.html')


def user_login(request):
    logout(request)
    if request.POST:
        user = authenticate(
            username=request.POST['meno'], password=request.POST['heslo'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('app:login'))
    return HttpResponseRedirect(reverse('app:login'))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:login'))


def remove_discussion(request, pk):
    Discussion.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('app:index'))


def add_discussion(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DiscussionForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                author = request.user
                time = datetime.datetime.now()
                discussion = Discussion(
                    title=title, description=description, author=author, date=time)
                discussion.save()
                return HttpResponseRedirect(reverse('app:index'))
        else:
            form = DiscussionForm()

        return render(request, 'app/form.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('app:login'))
