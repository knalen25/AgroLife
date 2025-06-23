from django.contrib import admin
from .models import ProtocoloSanitario, ProtocoloMedicamento

class ProtocoloMedicamentoInline(admin.TabularInline):
    model = ProtocoloMedicamento
    extra = 1
    fields = ('medicamento', 'dose_protocolo')
    autocomplete_fields = ('medicamento',)
    verbose_name = "Medicamento do Protocolo"
    verbose_name_plural = "Medicamentos do Protocolo"

@admin.register(ProtocoloSanitario)
class ProtocoloSanitarioAdmin(admin.ModelAdmin):
    list_display = ('idprotocolo_sanitario', 'nome_protocolo', 'motivo_protocolo', 'responsavel_tecnico')
    search_fields = ('nome_protocolo', 'motivo_protocolo', 'responsavel_tecnico__nome_responsavel')
    list_filter = ('responsavel_tecnico',)
    ordering = ('idprotocolo_sanitario',)
    autocomplete_fields = ('responsavel_tecnico',)
    inlines = [ProtocoloMedicamentoInline]

@admin.register(ProtocoloMedicamento)
class ProtocoloMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('idprotocolo_medicamento', 'protocolo_sanitario', 'medicamento', 'dose_protocolo')
    search_fields = ('protocolo_sanitario__nome_protocolo', 'medicamento__nome_medicamento')
    list_filter = ('protocolo_sanitario', 'medicamento')
    ordering = ('idprotocolo_medicamento',)
    autocomplete_fields = ('protocolo_sanitario', 'medicamento')