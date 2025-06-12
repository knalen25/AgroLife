from django import forms
from curral.models import Curral

class CurralModelForm(forms.ModelForm):
    
    class Meta:
        model = Curral
        fields = '__all__'