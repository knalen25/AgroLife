from django import forms
from movimentacao.models import Movimentacao

class TrocaCurralForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['data_movimentacao', 'status', 'lote_origem', 'lote_destino', 'curral_destino']
        widgets = {
            'data_movimentacao': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("lote_origem") == cleaned_data.get("lote_destino"):
            raise forms.ValidationError("O lote de origem e o lote de destino devem ser diferentes.")
        return cleaned_data
