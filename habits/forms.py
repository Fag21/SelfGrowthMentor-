from django import forms
from .models import Habit
from django.forms import Textarea

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'habit_type', 'reason', 'plan', 'commitment', 'goal_duration']
        widgets = {
            'reason': Textarea(attrs={'rows':3, 'placeholder':'Why do you want to change/build this habit?'}),
            'plan': Textarea(attrs={'rows':3, 'placeholder':'When, where and how will you do it? (implementation intent)'}),
        }

class HabitQuickForm(forms.ModelForm):
    """Small form for quick edits (used in list or quick-action)"""
    class Meta:
        model = Habit
        fields = ['commitment']
