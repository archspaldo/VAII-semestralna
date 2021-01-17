from django.core.checks import messages
from django.core import serializers
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Discussion, Comment
from django.views.generic import ListView
from .forms import DiscussionForm, LoginForm, ReplyForm
from urllib.parse import unquote
import json


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
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('app:login'))
        return render(request, 'app/login.html', {'form': form})

class DiscussionView(ListView):
    def get(self, request, pk):
        topic = Discussion.objects.filter(pk=pk).first()
        comments = Comment.objects.filter(discussion_id_id=pk, parent_id_id=None)
        is_authorized = request.user.is_superuser or request.user == topic.author
        return render(request, 'app/discussion.html', {'topic' : topic, 'comments': comments, 'is_authorized' : is_authorized,})

class EditView(View):
    def get(self, request, pk):
        discussion = Discussion.objects.filter(pk=pk).first()
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
            discussion.save()
        return HttpResponseRedirect(reverse('app:edit', args=(pk,)))


class AddView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = DiscussionForm()
            return render(request, 'app/add.html', {'form': form})
        return HttpResponseRedirect(reverse('app:login'))

    def post(self, request):
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = Discussion(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                author=request.user)
            discussion.save()
            return HttpResponseRedirect(reverse('app:edit', args=(discussion.id,)))


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
    
def get_comment(request, pk):
    if request.is_ajax() and request.method == 'GET':
        comment = Comment.objects.filter(pk = pk).first()
        comments = comment.get_comments(False)
        return JsonResponse({'comments': comments}, status=200)
    return JsonResponse({'error': ''}, status=400)

def reply(request):
    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        print(data)
        form = ReplyForm(data)
        if form.is_valid():
            comment = Comment(
                discussion_id = Discussion.objects.all().filter(pk=form.cleaned_data['topic']).first(),
                parent_id = Comment.objects.all().filter(pk=form.cleaned_data['parent_id']).first(),
                message = form.cleaned_data['message'],
                author = request.user,
            )
            comment.save()
            ser_comment = serializers.serialize('json', [comment,])[1:-1]
            return JsonResponse({'comment': ser_comment, 'author' : request.user.username}, status=200)
        return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': ''}, status=400)