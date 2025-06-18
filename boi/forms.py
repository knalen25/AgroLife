from django import forms
from boi.models import Boi, StatusBoi

class BoiModelForm(forms.ModelForm):
    class Meta:
        model = Boi
        fields = [
            "brinco",
            "chip",
            "fornecedor",
            "raca",
            "sexo",
            "peso_entrada",
            "data_nascimento",
            "data_entrada",
            "lote",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_entrada":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "brinco":          forms.TextInput(attrs={"class": "form-control"}),
            "chip":            forms.TextInput(attrs={"class": "form-control"}),
            "peso_entrada":    forms.NumberInput(attrs={"class": "form-control"}),
            "fornecedor":      forms.Select(attrs={"class": "form-control"}),
            "raca":            forms.Select(attrs={"class": "form-control"}),
            "sexo":            forms.Select(attrs={"class": "form-control"}),
            "lote":            forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        self.instance.status_boi = Boi.status_boi.ATIVO
        return super().save(commit=commit)

class BoiMorteForm(forms.ModelForm):
    status_boi = forms.ModelChoiceField(
        queryset=StatusBoi.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Status do Boi",
        help_text="Escolha 'Morto' para registrar a morte do animal."
    )

    class Meta:
        model = Boi
        fields = ["status_boi", "data_morte", "motivo_morte", "necropsia"]
        labels = {
            "data_morte":   "Data da Morte",
            "motivo_morte": "Motivo da Morte",
            "necropsia":    "Necropsia",
        }
        widgets = {
            "data_morte":   forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "motivo_morte": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status_boi")
        data_morte = cleaned.get("data_morte")
        motivo    = cleaned.get("motivo_morte")
        
        if status and status.nome_status == "Morto":
            if not data_morte:
                self.add_error("data_morte", 'Obrigatório ao marcar como "Morto".')
            if not motivo:
                self.add_error("motivo_morte", 'Obrigatório ao marcar como "Morto".')
        return cleaned

