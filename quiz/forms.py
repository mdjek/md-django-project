from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User


class SignUpForm(auth_forms.UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TestAccessForm(forms.Form):
    access_key = forms.CharField(max_length=50, label="Ключ доступа")