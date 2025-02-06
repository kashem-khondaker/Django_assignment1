from django import forms
from Participants.models import Participant
from events.forms import StyleFormMixin

class ParticipantForm(StyleFormMixin,forms.ModelForm):  
    class Meta:
        model = Participant  
        fields = ['name', 'email', 'events']  
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'}),
            'events': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets()