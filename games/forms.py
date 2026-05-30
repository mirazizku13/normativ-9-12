from django import forms
from .models import Game


class GameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        # fields = ('title_uz', 'title_ru', 'title_en', 'genre', 'price')
        fields = ('title', 'genre', 'price')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title_uz']
    #     if len(title) < 3:
    #         raise forms.ValidationError('Title kamida 3 ta harfdan iborat bo\'lishi kerak!')
    #     return title