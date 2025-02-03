from django import forms 
from Participants.models import Participant

class CategoriesForm:
    class Meta:
        models = Participant
        fields = ['name'  , 'description' ]
        widgets = {
            'name': forms.CharField(max_length=200),
            'description':  forms.Textarea(),
        }
    
    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)