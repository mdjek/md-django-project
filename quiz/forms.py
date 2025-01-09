from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Test

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class TestAccessForm(forms.Form):
    access_key = forms.CharField(max_length=50, label="Ключ доступа")