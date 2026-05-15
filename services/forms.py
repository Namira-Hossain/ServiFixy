from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'price', 'service_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }