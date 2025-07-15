from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from profiles.forms import ProfessionalProfileForm, CareerItemForm
from profiles.models import ProfessionalProfile, CareerItem
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


class CareerItemBaseView(View):
    allowed_types = ['education', 'experience']

    def dispatch(self, request, *args, **kwargs):
        self.item_type = kwargs.get('item_type')
        if self.item_type not in self.allowed_types:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CareerItem.objects.filter(fk_profile=self.request.user.profile, item_type=self.item_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = self.item_type
        return context


class CareerItemCreateView(CareerItemBaseView, FormView):
    form_class = CareerItemForm
    template_name = 'career-item-create.html'
    
    def form_valid(self, form):
        career_item = form.save(commit=False)
        career_item.fk_profile = self.request.user.profile
        career_item.item_type = self.item_type
        career_item.save()
        return redirect('profile')


class CareerItemUpdateView(CareerItemBaseView, UpdateView):
    model = CareerItem
    form_class = CareerItemForm
    template_name = 'career-item-edit.html'
    context_object_name = 'career_item'
    success_url = '/profile'


class CareerItemDeleteView(CareerItemBaseView, DeleteView):
    model = CareerItem
    template_name = 'career-item-delete.html'
    context_object_name = 'career_item'
    success_url = '/profile'
