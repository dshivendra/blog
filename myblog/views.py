from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

from django.http import HttpResponse
from django.http import Http404
# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'myblog/home.html', {'posts': posts})


def about(request):
    return render(request, 'myblog/about.html')


def contact(request):
    return render(request, 'myblog/contact.html')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                ups = form.cleaned_data['password']
                user = authenticate(username=uname, password=ups)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'logged in successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'myblog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congrats!! You are the journey of blogger ')
            user = form.save()
    else:
        form = SignupForm()
    return render(request, 'myblog/signup.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, 'myblog/dashboard.html', {'posts': posts})
    else:
        return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                assert isinstance(description, object)
                pst = Post(title=title, description=description)
                pst.save()
            else:
                form = PostForm()
        else:
            form = PostForm()
            return render(request, 'myblog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/dashboard")


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'myblog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
