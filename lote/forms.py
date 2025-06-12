from django import forms
from lote.models import Lote

class LoteModelForm(forms.ModelForm):

     class Meta:
        model = Lote
        fields = '__all__'