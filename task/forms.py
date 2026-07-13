from .models import Task
from django import forms

PRIORITY_CHOICES = [
    (0, 'Low'),
    (1, 'Medium'),
    (2, 'High'),
]

class TaskForm(forms.ModelForm):
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task description', 'rows': 3}),
        }