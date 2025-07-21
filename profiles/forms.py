from profiles.models import ProfessionalProfile, CareerItem
from technologies.models import Technology
from django import forms
from django_select2 import forms as s2forms
from datetime import date

class TechnologySelectWidget(s2forms.ModelSelect2MultipleWidget):
    model = Technology
    search_fields = ['name__istartswith']

class MonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        months = [
            ('', '--- Mes ---'),
            ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'),
            ('05', 'Mayo'), ('06', 'Junio'), ('07', 'Julio'), ('08', 'Agosto'),
            ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
        ]        
        current_year = date.today().year
        years = [('', '--- Año ---')] + [(str(year), str(year)) for year in range(1940, current_year + 1)]
        years.reverse()        
        widgets = [
            forms.Select(choices=months, attrs={'class': 'month-select'}),
            forms.Select(choices=years, attrs={'class': 'year-select'}),
        ] 
        
        super().__init__(widgets, attrs)

    # para render form
    def decompress(self, value):
        if value:
            return [value.strftime('%m'), value.strftime('%Y')]
        return [None, None]

    # para DB
    def value_from_datadict(self, data, files, name):
        month, year = super().value_from_datadict(data, files, name)
        if month and year:
            try:
                return date(int(year), int(month), 1)
            except ValueError:
                return None
        return None
        
    def format_output(self, rendered_widgets):
        return '<div class="month-year-widgets">{}</div>'.format(''.join(rendered_widgets))

class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = ['area', 'bio', 'technologies']
        widgets = {
            'area': forms.TextInput(attrs={
                'placeholder': 'Ej. Desarrollador Full Stack, Data Engineer, DevOps Specialist',
                'class': 'profile-form__area form-input'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Cuéntanos de ti...',
                'class': 'profile-form__bio form-input'
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
        fields = ['title', 'institution', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': ''
            }),
            'institution': forms.TextInput(attrs={
                'class': ''
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': ''
            }),
            'start_date': MonthYearWidget(),
            'end_date': MonthYearWidget(),
        }
        labels = {
            'title': 'Título',
            'institution': 'Nombre de la empresa o institución',
            'description': 'Descripción de tus responsabilidades y logros',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de finalización (dejar en blanco si es actual)',
        }
