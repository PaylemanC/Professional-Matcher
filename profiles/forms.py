from profiles.models import ProfessionalProfile, CareerItem
from technologies.models import Technology
from django import forms
from django_select2 import forms as s2forms

class TechnologySelectWidget(s2forms.ModelSelect2MultipleWidget):
    model = Technology
    search_fields = ['name__istartswith']

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
            'technologies': TechnologySelectWidget,
        }
        labels = {
            'bio': 'Describe tu experiencia profesional y objetivos',
            'area': 'Profesión',
            'technologies': 'Selecciona las tecnologías que dominas',
        } 

class CareerItemForm(forms.ModelForm):
    class Meta:
        model = CareerItem
        fields = ['title', 'description', 'institution', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': ''
            }),
            'institution': forms.TextInput(attrs={
                'class': ''
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': ''
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': ''
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': ''
            }),
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción de tus responsabilidades y logros',
            'institution': 'Nombre de la empresa o institución',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de finalización (dejar en blanco si es actual)',
        }
