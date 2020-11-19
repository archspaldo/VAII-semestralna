from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from .models import Discussion
from django.views.generic import ListView
from .forms import DiscussionForm, LoginForm


class IndexView(ListView):
    model = Discussion
    paginate_by = 10
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
            form = LoginForm()
            return render(request, 'app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
        return HttpResponseRedirect(reverse('app:login'))


class EditView(View):
    def get(self, request, pk):
        discussion = Discussion.objects.filter(pk=pk).first()
        if request.GET.get('error'):
            if request.GET.get('error') == '1':
                error = 'Neplatný názov'
            if request.GET.get('error') == '2':
                error = 'Zadaný názov už je použitý'
        if discussion is not None and (request.user.is_superuser or request.user == discussion.author):
            form = DiscussionForm()
        else:
            form = None
        return render(request, 'app/edit.html', {'discussion': discussion, 'form': form})

    def post(self, request, pk):
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = Discussion(
                id=pk,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                author=request.user)
            try:
                discussion.save()
            except:
                return HttpResponseRedirect("?error=2")
        return HttpResponseRedirect(reverse('app:edit', args=(pk,)))


class AddView(View):
    def get(self, request):
        if request.user.is_authenticated:
            error = None
            if request.GET.get('error'):
                if request.GET.get('error') == '1':
                    error = 'Neplatný názov'
                if request.GET.get('error') == '2':
                    error = 'Zadaný nźov už je použitý'
            form = DiscussionForm()
            return render(request, 'app/add.html', {'form': form, 'error': error})
        return HttpResponseRedirect(reverse('app:login'))

    def post(self, request):
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = Discussion(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                author=request.user)
            try:
                discussion.save()
            except:
                return HttpResponseRedirect("?error=2")
            return HttpResponseRedirect(reverse('app:edit', args=(discussion.id,)))
        return HttpResponseRedirect("?error=1")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:login'))


def remove_discussion(request, pk):
    if request.user.is_authenticated:
        discussion = Discussion.objects.filter(pk=pk).first()
        if (discussion is not None) and (request.user.is_superuser or request.user == discussion.author):
            discussion.delete()
        return HttpResponseRedirect(reverse('app:index'))
    else:
        return HttpResponseRedirect(reverse('app:login'))
