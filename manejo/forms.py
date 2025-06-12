from django import forms
from django.forms import inlineformset_factory, modelformset_factory

# Importe todos os modelos necessários
from .models import Manejo, ParametroManejo, BoiManejo
from boi.models import Boi

# ===================================================================
# 1. FORMULÁRIO PRINCIPAL DO MANEJO
# ===================================================================

class ManejoForm(forms.ModelForm):
    """
    Formulário para os dados principais do Manejo.
    O widget 'tipo_manejo' tem um ID específico ('id_tipo_manejo')
    para que o JavaScript no template possa identificá-lo e alternar
    os formsets de bois dinamicamente.
    """
    class Meta:
        model = Manejo
        fields = ['tipo_manejo', 'status_manejo', 'data_manejo', 'protocolo_sanitario']
        widgets = {
            'data_manejo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_manejo': forms.Select(attrs={'id': 'id_tipo_manejo', 'class': 'form-control'}),
            'status_manejo': forms.Select(attrs={'class': 'form-control'}),
            'protocolo_sanitario': forms.Select(attrs={'class': 'form-control'}),
        }

# ===================================================================
# 2. FORMSET PARA OS PARÂMETROS DE MANEJO
# ===================================================================

class ParametroManejoForm(forms.ModelForm):
    """Formulário para cada linha de parâmetro (regra) do manejo."""
    class Meta:
        model = ParametroManejo
        fields = ['lote', 'raca', 'peso_inicial', 'peso_final']
        widgets = {
            'lote': forms.Select(attrs={'class': 'form-control'}),
            'raca': forms.Select(attrs={'class': 'form-control'}),
            'peso_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso_final': forms.NumberInput(attrs={'class': 'form-control'}),
        }

ParametroManejoFormSet = inlineformset_factory(
    Manejo,
    ParametroManejo,
    form=ParametroManejoForm,
    fk_name='manejo',  # Boa prática especificar a chave estrangeira
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

# ===================================================================
# 3. FORMSET PARA SELECIONAR BOIS EXISTENTES (MOVIMENTAÇÃO/VENDA)
# ===================================================================

class BoiManejoForm(forms.ModelForm):
    """
    Formulário para cada linha de boi SELECIONADO.
    Inclui campos desabilitados para mostrar os dados do boi escolhido.
    """
    brinco = forms.CharField(disabled=True, required=False, label='Brinco')
    chip = forms.CharField(disabled=True, required=False, label='Chip')
    peso_entrada = forms.DecimalField(disabled=True, required=False, label='Peso Atual')
    peso_saida = forms.DecimalField(disabled=True, required=False, label='Peso Saída')
    data_nascimento = forms.DateField(disabled=True, required=False, label='Nascimento')
    data_entrada = forms.DateField(disabled=True, required=False, label='Entrada')
    data_saida = forms.DateField(disabled=True, required=False, label='Saída')
    sexo = forms.CharField(disabled=True, required=False, label='Sexo')
    fornecedor = forms.CharField(disabled=True, required=False, label='Fornecedor')
    raca = forms.CharField(disabled=True, required=False, label='Raça')
    lote = forms.CharField(disabled=True, required=False, label='Lote Atual')
    status = forms.CharField(disabled=True, required=False, label='Status')

    class Meta:
        model = BoiManejo
        fields = ['boi']
        widgets = {
            'boi': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Otimiza a consulta para carregar dados relacionados de uma só vez
        self.fields['boi'].queryset = Boi.objects.select_related(
            'raca', 'lote', 'sexo', 'fornecedor', 'status_boi'
        ).order_by('brinco')

        # Preenche os campos desabilitados se um boi já estiver selecionado
        if self.instance and hasattr(self.instance, 'boi') and self.instance.boi:
            b = self.instance.boi
            self.fields['brinco'].initial = b.brinco
            self.fields['chip'].initial = b.chip
            self.fields['peso_entrada'].initial = b.peso_entrada
            self.fields['peso_saida'].initial = b.peso_saida
            self.fields['data_nascimento'].initial = b.data_nascimento
            self.fields['data_entrada'].initial = b.data_entrada
            self.fields['data_saida'].initial = b.data_saida
            self.fields['sexo'].initial = b.sexo.tipo_sexo if b.sexo else ''
            self.fields['fornecedor'].initial = b.fornecedor.nome_fornecedor if b.fornecedor else ''
            self.fields['raca'].initial = b.raca.nome_raca if b.raca else ''
            self.fields['lote'].initial = b.lote.nome_lote if b.lote else ''
            self.fields['status'].initial = b.status_boi.nome_status if b.status_boi else ''

BoiManejoFormSet = inlineformset_factory(
    Manejo,
    BoiManejo,
    form=BoiManejoForm,
    fk_name='manejo',
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

# ===================================================================
# 4. FORMSET PARA CRIAR NOVOS BOIS (ENTRADA)
# ===================================================================

class BoiEntradaForm(forms.ModelForm):
    """
    Formulário para CADASTRAR um novo Boi durante o manejo de entrada.
    Os campos aqui são editáveis.
    """
    class Meta:
        model = Boi
        # Campos necessários para cadastrar um novo boi no sistema
        fields = [
            'brinco', 'raca', 'sexo', 'data_nascimento', 'data_entrada',
            'peso_entrada', 'fornecedor', 'status_boi'
        ]
        widgets = {
            'brinco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brinco do animal'}),
            'raca': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'peso_entrada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso em kg'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'status_boi': forms.Select(attrs={'class': 'form-control'}),
        }

# Usamos `modelformset_factory` porque estamos criando instâncias do modelo `Boi` diretamente,
# e não de um modelo de junção (como BoiManejo).
BoiEntradaFormSet = modelformset_factory(
    Boi,
    form=BoiEntradaForm,
    extra=1,
    can_delete=True,
)