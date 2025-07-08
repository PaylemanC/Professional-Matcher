from django.db import models

class ProfessionalProfile(models.Model):
    bio = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CareerItem(models.Model):
    fk_profile = models.ForeignKey(ProfessionalProfile, related_name='career_items', on_delete=models.CASCADE)
    item_type = models.CharField(choices=[('education', 'Education'), ('experience', 'Experience')])
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True, default="Independent")
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def get_end_date_display(self):
        if self.end_date:
            return self.end_date.strftime("%B %Y")
        return "Present"

    def __str__(self):
        return f"{self.title} at {self.institution} ({self.start_date} - {self.end_date})"
