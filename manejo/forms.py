from django import forms
from django.forms import inlineformset_factory
from .models import Manejo, ParametroManejo, TipoManejo, StatusManejo
from boi.models import Boi
from lote.models import Lote

# Formulário para os detalhes do Manejo
class ManejoForm(forms.ModelForm):
    # Forçamos a seleção do tipo de manejo para 'entrada' nesta view específica
    tipo_manejo = forms.ModelChoiceField(
        queryset=TipoManejo.objects.filter(nome_tipo_manejo='Entrada'),
        empty_label=None # Remove a opção "---------"
    )
    data_manejo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data do Manejo")

    class Meta:
        model = Manejo
        fields = ['data_manejo', 'tipo_manejo', 'protocolo_sanitario']


# Formulário para cada regra/parâmetro
class ParametroManejoForm(forms.ModelForm):
    class Meta:
        model = ParametroManejo
        fields = ['lote', 'raca', 'peso_inicial', 'peso_final']

# FormSet para criar múltiplos parâmetros dentro do formulário de Manejo
ParametroManejoFormSet = inlineformset_factory(
    Manejo,                # Modelo Pai
    ParametroManejo,       # Modelo Filho
    form=ParametroManejoForm,
    extra=1,               # Começa com 1 formulário de parâmetro
    can_delete=True,
    fk_name='manejo'
)


# Formulário para cada Boi (semelhante ao anterior)
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

# FormSet para os Bois (não é 'inline' pois o vínculo é feito na view)
BoiEntradaFormSet = forms.formset_factory(BoiEntradaForm, extra=1, can_delete=True)






class SelecaoLoteForm(forms.Form):
    """Formulário simples para o usuário escolher de qual lote vender o gado."""
    lote = forms.ModelChoiceField(
        queryset=Lote.objects.filter(ativo=True), # Mostra apenas lotes ativos
        label="Selecione o Lote para a Venda",
        help_text="Apenas os animais ativos deste lote serão listados."
    )

class BoiSaidaForm(forms.Form):
    """
    Formulário para capturar os dados de saída de um único boi.
    Não é um ModelForm porque não estamos criando, e sim atualizando
    campos específicos de um Boi que já existe.
    """
    # Usamos um campo oculto para saber a qual boi estes dados pertencem.
    # A view se encarregará de preencher este campo.
    boi_id = forms.IntegerField(widget=forms.HiddenInput())
    
    # Checkbox para o usuário marcar quais bois do lote ele quer vender.
    selecionado = forms.BooleanField(required=False, label="Vender este animal")

    peso_saida = forms.DecimalField(
        label="Peso de Saída (kg)", 
        required=False, # Não é obrigatório até que o checkbox seja marcado
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 450.50'})
    )
    data_saida = forms.DateField(
        label="Data da Saída", 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # Você poderia adicionar aqui `preco_venda`, `comprador`, etc. se modificar o modelo.

    def clean(self):
        """
        Validação customizada: se o boi foi selecionado para venda,
        então o peso e a data de saída se tornam obrigatórios.
        """
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


# Criamos um FormSet para a lista de bois
BoiSaidaFormSet = forms.formset_factory(BoiSaidaForm, extra=0)


class BuscaBoiForm(forms.Form):
    """Formulário super simples para buscar um boi."""
    brinco = forms.CharField(
        label="Digite o Brinco do Boi",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Busca exata...', 'autofocus': True})
    )

class VendaBoiForm(forms.Form):
    """
    Formulário para os dados de saída. Aparecerá DEPOIS que um boi for encontrado.
    """
    boi_id = forms.IntegerField(widget=forms.HiddenInput()) # Campo oculto com o ID do boi
    
    # Detalhes da venda para este boi específico
    peso_saida = forms.DecimalField(label="Peso de Saída (kg)", required=True)
    data_saida = forms.DateField(label="Data da Saída", required=True, widget=forms.DateInput(attrs={'type': 'date'}))
