from django import forms 
from Participants.models import Participant

class ParticipantsForm(forms.Form):
    class Meta:
        models = Participant
        fields = ['name'  , 'email'  , 'events']
        widgets = {
            'name': forms.CharField(max_length=200),
            'email': forms.EmailField(unique=True),
            'events':forms.CheckboxSelectMultiple,
        }
    
    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
