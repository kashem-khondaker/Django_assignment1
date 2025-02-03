from django import forms
from events.models import Event
from categories.models import Categories

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category'] 
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter event title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter event description', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter event location', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
