from django import forms
from Participants.models import Participant
from events.forms import StyleFormMixin
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User , Permission , Group



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

class RegistrationsForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' ,'first_name' , 'last_name' , 'email', 'password1' , 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm , self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CreateGroupForm(StyleFormMixin , forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name','permissions']

class AssignedRoleForm(StyleFormMixin , forms.Form):
    Role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label="select a role "
    )

