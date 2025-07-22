from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from technologies.models import Technology

class ProfessionalProfile(models.Model):
    fk_user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    technologies = models.ManyToManyField(Technology, blank=True, related_name='profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fk_user.username}'s Profile"
    
    def clean(self):
        errors = {}
        
        if not self.area or self.area.strip() == "" or self.area is None:
            errors['area'] = "*Campo obligatorio."
        elif len(self.area) > 100:
            errors['area'] = "*Máximo 100 caracteres."
        if self.bio and len(self.bio) > 750:
            errors['bio'] = "*Máximo 750 caracteres."

        if errors:
            raise ValidationError(errors)

class CareerItem(models.Model):
    fk_profile = models.ForeignKey(ProfessionalProfile, related_name='career_items', on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=[('education', 'Education'), ('experience', 'Experience')])
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True, default="Independiente")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"({self.fk_profile.fk_user}) {self.title} at {self.institution} ({self.start_date} - {self.end_date})"    
    
    def get_end_date_display(self):
        if self.end_date:
            return self.end_date.strftime("%B %Y")
        return "Actualidad"

    def clean(self):
        errors = {}

        if not self.title or self.title.strip() == "" or self.title is None:
            errors['title'] = "*Campo obligatorio."

        if not self.start_date or self.start_date is None:
            errors['start_date'] = "*Campo obligatorio."

        if not self.institution or self.institution.strip() == "" or self.institution is None:
            errors['institution'] = "*Campo obligatorio."

        if self.title and len(self.title) > 200:
            errors['title'] = "Máximo 200 caracteres."

        if self.institution and len(self.institution) > 200:
            errors['institution'] = "Máximo 200 caracteres."

        if self.description and len(self.description) > 1100:
            errors['description'] = "Máximo 1100 caracteres."

        if self.end_date and self.end_date < self.start_date:
            errors['end_date'] = "La fecha de finalización no puede ser anterior a la fecha de inicio."

        if errors:
            raise ValidationError(errors)