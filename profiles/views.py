from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_detail(request):
    profile = getattr(request.user, 'profile', None)
    
    return render(request, 'profile.html', {'profile': profile})
