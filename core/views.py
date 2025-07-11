from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index') 
    return render(request, 'dashboard.html')
