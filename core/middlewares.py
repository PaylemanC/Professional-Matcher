from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from profiles.models import ProfessionalProfile

class EnsureProfileOnPostMiddleware:
    """
    Intercepts POST forms submission and checks 
    if the user has a professional profile.
    If not, it redirects to the profile creation page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.user.is_authenticated:
            has_profile = ProfessionalProfile.objects.filter(fk_user=request.user).exists()
            if not has_profile:
                messages.warning(
                    request, "Debes crear un perfil profesional antes de empezar a usar el análisis."
                )
                return redirect(reverse("profile_create"))

        return self.get_response(request)
