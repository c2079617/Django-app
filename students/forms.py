from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Enter a valid student email')
    student_id = forms.CharField(label='Student ID', max_length=100, help_text='Enter your unique student ID')

    class Meta:
        model = User
        fields = ['username', 'email', 'student_id', 'password1', 'password2']