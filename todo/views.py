import django.contrib.admin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request, 'todo/home.html')

def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {'form': UserCreationForm(),
                               'error': "That name has already been taken. Please choose a new username"})
        else:
            return render(request, 'todo/signup_user.html',
                          {'form':UserCreationForm(), 'error':"Passwords didn't match"})

def current_todos(request):
    return render(request, 'todo/current_todos.html')

def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html',
                          {'form': AuthenticationForm(), 'error': "Username and password didn't match"})
        else:
            login(request, user)
            return redirect('current_todos')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')