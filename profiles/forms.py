from profiles.models import ProfessionalProfile, CareerItem
from django import forms

class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = ['area', 'bio', 'technologies']
        widgets = {
            'area': forms.TextInput(attrs={
                'placeholder': 'Ej. Desarrollador Full Stack, Data Engineer, DevOps Specialist',
                'class': ''
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Cuéntanos de ti...',
                'class': ''
            }),
            'technologies': forms.CheckboxSelectMultiple(attrs={
                'class': ''
            }),
        }
        labels = {
            'bio': 'Describe tu experiencia profesional y objetivos',
            'area': 'Profesión',
            'technologies': 'Selecciona las tecnologías que dominas',
        } 
