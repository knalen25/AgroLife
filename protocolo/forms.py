from django import forms
from django.forms import inlineformset_factory
from protocolo.models import ProtocoloSanitario, ProtocoloMedicamento

class ProtocoloSanitarioForm(forms.ModelForm):
    class Meta:
        model = ProtocoloSanitario
        fields = ['nome_protocolo', 'motivo_protocolo', 'responsavel_tecnico']

class ProtocoloMedicamentoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloMedicamento
        fields = ['medicamento', 'dose_protocolo']

ProtocoloMedicamentoFormSet = inlineformset_factory(
    ProtocoloSanitario,
    ProtocoloMedicamento,
    form=ProtocoloMedicamentoForm,
    extra=1,
    can_delete=True
)
