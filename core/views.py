from django.shortcuts import render, redirect
from django.contrib import messages
from matching.forms import JobOfferForm
from matching.services.matcher import MatcherService
from profiles.models import ProfessionalProfile

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index') 
    
    try:
        request.user.profile
    except ProfessionalProfile.DoesNotExist:
        messages.warning(request, 'Debes crear un perfil profesional antes de usar el matcher.')
        return redirect('profile_create')
    
    form = JobOfferForm()
    match_results = None
    
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job_text = form.cleaned_data['job_offer']
            
            try:
                matcher = MatcherService(request.user, job_text)
                
                overall_score = matcher.match()
                
                match_results = {
                    'overall_score': overall_score,
                    'technology_match': matcher.technology_match_results,
                    'keyword_match': matcher.keyword_match_results,
                    'career_items': matcher.career_items_results,
                    'missing_elements': matcher.missing_elements_results,
                    'job_offer': job_text
                }
                
                messages.success(request, f'Análisis completado. Puntuación de compatibilidad: {overall_score}%')
                
            except Exception as e:
                messages.error(request, f'Error al procesar la oferta laboral: {str(e)}')
                match_results = None

    return render(request, 'dashboard.html', { 
                'form': form, 
                'match_results': match_results
            })
