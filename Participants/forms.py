from django import forms
from Participants.models import Participant

class ParticipantForm(forms.ModelForm):  
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
