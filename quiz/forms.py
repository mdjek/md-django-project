from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from .models import Subject, Test

class SignUpForm(auth_forms.UserCreationForm):
    is_admin = forms.BooleanField(required=False, label="Зарегистрироваться как администратор")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_admin')

class TestForm(forms.ModelForm):
    new_subject = forms.CharField(max_length=100, required=False, label="Новый предмет")

    class Meta:
        model = Test
        fields = ['subject', 'name', 'pass_score', 'start_time', 'end_time', 'duration']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        new_subject = cleaned_data.get('new_subject')

        if not subject and not new_subject:
            raise forms.ValidationError("Выберите существующий предмет или введите новый.")
        
        if new_subject:
            subject, created = Subject.objects.get_or_create(name=new_subject)
            cleaned_data['subject'] = subject

        return cleaned_data


class TestAccessForm(forms.Form):
    access_key = forms.CharField(max_length=50, label="Ключ доступа")