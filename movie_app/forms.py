from .models import Movie
from django import forms
from django.forms import TextInput, NumberInput


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'rating']
        labels = {
            'name': "Название:",
            'rating': 'Рейтинг:',
        }
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Введите название фильма'
            }),
            'rating': NumberInput(attrs={
                'placeholder': 'Введите рейтинг'
            }),
            }
