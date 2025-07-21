from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from users.forms import CustomLoginForm, CustomUserCreationForm

def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home') 
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
