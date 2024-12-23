from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(validators=[EmailValidator()], required=True)
    phone = forms.CharField(max_length=15, required=True)
    subject = forms.CharField(max_length=100, required=True)
    room = forms.CharField(max_length=10, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)