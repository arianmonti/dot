from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.shortcuts import redirect, render

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
