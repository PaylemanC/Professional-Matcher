from django.shortcuts import render, redirect
from matching.forms import JobOfferForm

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index') 
    
    form = JobOfferForm()
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
           job_text = form.cleaned_data['job_offer']
           result = job_text.upper()

    return render(request, 'dashboard.html', { 
                'form': form, 
                'result': result if 'result' in locals() else None
            })
