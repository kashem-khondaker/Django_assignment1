from django import forms
from events.models import Event
from categories.models import Categories

from django import forms
from .models import Event

# class StyleFormMixin:
    
#     common_class = "w-full border border-gray-300 rounded-lg shadow-md py-3 px-4 mt-2 mb-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 ease-in-out"

#     def apply_style_widgets(self):

#         for field_name, field in self.fields.items():
#             if isinstance(field.widget, forms.TextInput):
#                 field.widget.attrs.update({
#                     'class': self.common_class,
#                     'placeholder': f"Enter {field.label.lower()}",
#                 })
#             elif isinstance(field.widget, forms.Textarea):
#                 field.widget.attrs.update({
#                     'class': f"{self.common_class} resize-none",
#                     'placeholder': f"Enter {field.label.lower()}",
#                     'rows': 5
#                 })
#             elif isinstance(field.widget, forms.DateInput):
#                 field.widget.attrs.update({
#                     'class': f"{self.common_class} bg-white",
#                     'type': 'date'
#                 })
#             elif isinstance(field.widget, forms.TimeInput):
#                 field.widget.attrs.update({
#                     'class': f"{self.common_class} bg-white",
#                     'type': 'time'
#                 })
#             elif isinstance(field.widget, forms.Select):
#                 field.widget.attrs.update({
#                     'class': f"{self.common_class} bg-white cursor-pointer",
#                 })
#             elif isinstance(field.widget, forms.CheckboxSelectMultiple):
#                 field.widget.attrs.update({
#                     'class': "rounded-md  mt-2 mb-4 "
#                 })
#             else:
#                 field.widget.attrs.update({
#                     'class': self.common_class
#                 })

class StyleFormMixin:
    
    common_class = "w-full border border-gray-600 bg-gray-800 text-white rounded-lg shadow-md py-3 px-4 mt-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 ease-in-out"
    label_class = "block text-white text-sm font-semibold mb-2"

    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': self.common_class})
            
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'placeholder': f"Enter {field.label.lower()}"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'placeholder': f"Enter {field.label.lower()}", 'rows': 5})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'type': 'date'})
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({'type': 'time'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': f"{self.common_class} bg-gray-900 cursor-pointer"})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': "rounded-md mt-2 mb-4 text-white"})
            
            # Update label styling
            if field.label:
                field.label_attrs = {'class': self.label_class}

# --------- Event Form with Modern Tailwind Design --------- #
class EventForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category' , 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets()
