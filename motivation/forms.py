from django import forms
from .models import Motive

class MotiveForm(forms.ModelForm):
    class Meta:
        model = Motive
        fields = ['title', 'description', 'reward', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }



