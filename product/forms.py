from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('5 ta harifdan kotabo`lsinx')


    def clean(self):
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']

        if title == description:
            raise forms.ValidationError('title va description bir xil malumot kiritmang!')
        return self.cleaned_data