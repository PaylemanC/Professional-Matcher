from django import forms

class JobOfferForm(forms.Form):
    job_offer = forms.CharField(widget=forms.Textarea, label='', required=True)