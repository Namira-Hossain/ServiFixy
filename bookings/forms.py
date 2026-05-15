from django import forms
from .models import Booking, Rating

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
        }