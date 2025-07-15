from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from profiles.forms import ProfessionalProfileForm
from profiles.models import ProfessionalProfile
from django.views.generic.edit import UpdateView, FormView, DeleteView

@login_required
def profile_detail(request):
    profile = getattr(request.user, 'profile', None)
    
    return render(request, 'profile.html', {'profile': profile})


class ProfileCreateView(FormView):
    form_class = ProfessionalProfileForm
    template_name = 'profile-create.html'
    success_url = '/profile'
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        # profile.user = self.request.user
        profile.fk_user = self.request.user
        profile.save()
        form.save_m2m() 
        return redirect('profile')


class ProfileUpdateView(UpdateView):
    model = ProfessionalProfile
    form_class = ProfessionalProfileForm
    template_name = 'profile-edit.html'
    success_url = '/profile'

    def get_object(self):
        return self.request.user.profile
