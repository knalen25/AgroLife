from django import forms
from django.forms import inlineformset_factory
from manejo.models import Manejo, ParametroManejo, TipoManejo, StatusManejo
from protocolo.models import ProtocoloSanitario
from boi.models import Boi
from lote.models import Lote

class ManejoForm(forms.ModelForm):
    tipo_manejo = forms.ModelChoiceField(
        queryset=TipoManejo.objects.filter(nome_tipo_manejo='Entrada'),
        empty_label=None
    )
    data_manejo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data do Manejo")

    class Meta:
        model = Manejo
        fields = ['data_manejo', 'tipo_manejo', 'protocolo_sanitario']

class ParametroManejoForm(forms.ModelForm):
    class Meta:
        model = ParametroManejo
        fields = ['lote', 'raca', 'peso_inicial', 'peso_final']

ParametroManejoFormSet = inlineformset_factory(
    Manejo,
    ParametroManejo,
    form=ParametroManejoForm,
    extra=1,
    can_delete=True,
    fk_name='manejo'
)

class BoiEntradaForm(forms.ModelForm):
    class Meta:
        model = Boi
        fields = [
            'brinco', 'chip', 'peso_entrada', 'data_nascimento', 
            'data_entrada', 'sexo', 'raca', 'fornecedor'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['peso_entrada'].required = True

BoiEntradaFormSet = forms.formset_factory(BoiEntradaForm, extra=1, can_delete=True)

class SelecaoLoteForm(forms.Form):
    lote = forms.ModelChoiceField(
        queryset=Lote.objects.filter(ativo=True),
        label="Selecione o Lote para a Venda",
        help_text="Apenas os animais ativos deste lote serão listados."
    )

class BoiSaidaForm(forms.Form):
    boi_id = forms.IntegerField(widget=forms.HiddenInput())
    selecionado = forms.BooleanField(required=False, label="Vender este animal")

    peso_saida = forms.DecimalField(
        label="Peso de Saída (kg)", 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 450.50'})
    )
    data_saida = forms.DateField(
        label="Data da Saída", 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        selecionado = cleaned_data.get("selecionado")
        peso_saida = cleaned_data.get("peso_saida")
        data_saida = cleaned_data.get("data_saida")

        if selecionado:
            if not peso_saida:
                self.add_error('peso_saida', 'Este campo é obrigatório para animais vendidos.')
            if not data_saida:
                self.add_error('data_saida', 'Este campo é obrigatório para animais vendidos.')
        
        return cleaned_data

BoiSaidaFormSet = forms.formset_factory(BoiSaidaForm, extra=0)


class BuscaBoiForm(forms.Form):
    brinco = forms.CharField(
        label="Digite o Brinco do Boi",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Busca exata...', 'autofocus': True})
    )

class VendaBoiForm(forms.Form):
    boi_id = forms.IntegerField(widget=forms.HiddenInput())
    
    peso_saida = forms.DecimalField(label="Peso de Saída (kg)", required=True)
    data_saida = forms.DateField(label="Data da Saída", required=True, widget=forms.DateInput(attrs={'type': 'date'}))

class ManejoForm(forms.ModelForm):
    data_manejo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data do Manejo")
    protocolo_sanitario = forms.ModelChoiceField(
        queryset=ProtocoloSanitario.objects.all(),
        label="Protocolo Sanitário",
        required=True
    )
    
    class Meta:
        model = Manejo
        fields = ['data_manejo', 'protocolo_sanitario']

class ParametroMovimentacaoForm(forms.ModelForm):
    class Meta:
        model = ParametroManejo
        fields = ['lote', 'raca', 'peso_inicial', 'peso_final']

class BuscaBoiForm(forms.Form):
    brinco = forms.CharField(label="Buscar pelo Brinco", max_length=20)

class MovimentacaoDataForm(forms.Form):
    boi_id = forms.IntegerField(widget=forms.HiddenInput())
    peso_movimentacao = forms.DecimalField(label="Novo Peso (kg)", required=True)

from django.forms import inlineformset_factory

ParametroMovimentacaoFormSet = inlineformset_factory(
    Manejo, ParametroManejo, form=ParametroMovimentacaoForm,
    extra=1, can_delete=True, fk_name='manejo',
)

class ManejoUpdateForm(forms.ModelForm):
    class Meta:
        model = Manejo
        fields = ['status_manejo', 'data_manejo', 'protocolo_sanitario']