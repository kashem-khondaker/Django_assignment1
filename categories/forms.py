from django import forms 
from categories.models import Categories
from events.forms import StyleFormMixin

class CategoriesForm( StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name'  , 'description' ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={ 'rows': 4, 'placeholder': 'Enter description'}),
        }
    
    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.apply_style_widgets()