from django.db import models

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']
