from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm
from .models import Post


@login_required(login_url='/login/')
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.return_user()
            login_user(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})


def logout(request):
    logout_user(request)
    return redirect('/')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.create_user()
            return redirect('/login/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})