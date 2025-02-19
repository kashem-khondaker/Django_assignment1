from django import forms
from Participants.models import Participant
from events.forms import StyleFormMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Permission, Group


class ParticipantForm(StyleFormMixin, forms.ModelForm):  
    class Meta:
        model = Participant  
        fields = ['name', 'email', 'events']  
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'events': forms.CheckboxSelectMultiple(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets()


class RegistrationsForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.apply_style_widgets()  

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None


class CreateGroupForm(StyleFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets() 


class AssignedRoleForm(StyleFormMixin, forms.Form):
    Role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets()  