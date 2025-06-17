from django import forms
from django.forms import inlineformset_factory
from .models import Medicamento, AplicacaoEvento, MedicamentoAplicado

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'nome_medicamento',
            'dias_de_carencia',
            'preco_ml',
            'tipo_medicamento',
            'principio_ativo',
            'laboratorio'
        ]


class AplicacaoEventoForm(forms.ModelForm):
    class Meta:
        model = AplicacaoEvento
        fields = [
            'data_aplicacao_medicamento',
            'boi',
            'doenca',
            'responsavel_tecnico'
        ]


class MedicamentoAplicadoForm(forms.ModelForm):
    class Meta:
        model = MedicamentoAplicado
        fields = [
            'medicamento',
            'dose_aplicada'
        ]


MedicamentoAplicadoFormSet = inlineformset_factory(
    AplicacaoEvento,
    MedicamentoAplicado,
    form=MedicamentoAplicadoForm,
    extra=1,
    can_delete=False
)
