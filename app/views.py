from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import Post


@login_required(login_url='/login/')
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'username or password is incorrect.')
            return redirect('/login')
        login_user(request, user)
        return redirect('/')
    return render(request, 'login.html')


def logout(request):
    logout_user(request)
    return redirect('/')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user = User.objects.filter(username=username).first()
        user_email = User.objects.filter(username=username).first()
        if user is not None or user_email is not None:
            messages.error(request, 'user exists.')
        if password != confirm_password:
            messages.error(request, 'passwords are not same.')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        return redirect('/login/')
    return render(request, 'register.html')
