from django import forms 
from events.models import Event

class EventForm:
    class Meta:
        model = Event
        fields = ['title' , 'description' , 'date' , 'time' , 'location' , 'category']
        widgets= {
            'title': forms.CharField(max_length=250 , label='Title'),
            'description' : forms.Textarea(),
            'date': forms.SelectDateWidget,
        }
        # in-complete ...
    def __init__(self, *args, **kwargs):
        super().__init__( *args , **kwargs)