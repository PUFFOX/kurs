# Імпортуємо базові елементи Django Forms
from django import forms
from .models import StudyGroup

# Кастомна форма реєстрації з полями: логін, пароль, ім’я, прізвище, група
class CustomRegisterForm(forms.Form):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Ім’я", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(
        label="Номер групи",
        queryset=StudyGroup.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
