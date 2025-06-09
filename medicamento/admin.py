from django.contrib import admin
from .models import (
    Doenca,
    ResponsavelTecnico,
    TipoMedicamento,
    PrincipioAtivo,
    Laboratorio,
    Medicamento,
    AplicacaoEvento,
    MedicamentoAplicado,
)

#
# Inline para MedicamentoAplicado dentro de AplicacaoEvento
#
class MedicamentoAplicadoInline(admin.TabularInline):
    model = MedicamentoAplicado
    extra = 1
    fields = (
        'medicamento',
        'dose_aplicada',
    )
    autocomplete_fields = ('medicamento',)
    verbose_name = "Medicamento Aplicado"
    verbose_name_plural = "Medicamentos Aplicados"


#
# Admin para AplicacaoEvento
#
@admin.register(AplicacaoEvento)
class AplicacaoEventoAdmin(admin.ModelAdmin):
    list_display = (
        'idaplicacao_evento',
        'data_aplicacao_medicamento',
        'boi',
        'doenca',
        'responsavel_tecnico',
    )
    list_filter = (
        'data_aplicacao_medicamento',
        'doenca',
        'responsavel_tecnico',
    )
    search_fields = (
        'boi__brinco',
        'doenca__nome_doenca',
        'responsavel_tecnico__nome_responsavel',
    )
    date_hierarchy = 'data_aplicacao_medicamento'
    autocomplete_fields = (
        'boi',
        'doenca',
        'responsavel_tecnico',
    )
    inlines = [MedicamentoAplicadoInline]
    raw_id_fields = ()  # caso queira usar raw_id em vez de autocomplete
    ordering = ('-data_aplicacao_medicamento', 'boi')

    fieldsets = (
        (None, {
            'fields': (
                'data_aplicacao_medicamento',
                'boi',
                'doenca',
                'responsavel_tecnico',
            ),
        }),
    )


#
# Admin para MedicamentoAplicado (caso queira gerenciar separadamente)
#
@admin.register(MedicamentoAplicado)
class MedicamentoAplicadoAdmin(admin.ModelAdmin):
    list_display = (
        'idmedicamento_aplicado',
        'evento',
        'medicamento',
        'dose_aplicada',
    )
    list_filter = (
        'medicamento',
        'evento__data_aplicacao_medicamento',
    )
    search_fields = (
        'evento__boi__brinco',
        'medicamento__nome_medicamento',
    )
    autocomplete_fields = (
        'evento',
        'medicamento',
    )
    ordering = ('evento', 'medicamento')


#
# Admin para Medicamento
#
@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = (
        'idmedicamento',
        'nome_medicamento',
        'tipo_medicamento',
        'principio_ativo',
        'laboratorio',
        'dias_de_carencia',
        'preco_ml',
    )
    list_filter = (
        'tipo_medicamento',
        'principio_ativo',
        'laboratorio',
    )
    search_fields = (
        'nome_medicamento',
        'principio_ativo__nome_principio_ativo',
        'laboratorio__nome_laboratorio',
    )
    autocomplete_fields = (
        'tipo_medicamento',
        'principio_ativo',
        'laboratorio',
    )
    ordering = ('nome_medicamento',)

    fieldsets = (
        (None, {
            'fields': (
                'nome_medicamento',
                'tipo_medicamento',
                'principio_ativo',
                'laboratorio',
            ),
        }),
        ('Detalhes Financeiros / Técnicos', {
            'fields': (
                'dias_de_carencia',
                'preco_ml',
            ),
            'classes': ('collapse',),
        }),
    )


#
# Admin para TipoMedicamento
#
@admin.register(TipoMedicamento)
class TipoMedicamentoAdmin(admin.ModelAdmin):
    list_display = (
        'idtipo_medicamento',
        'nome_medicamento',
    )
    search_fields = ('nome_medicamento',)
    ordering = ('nome_medicamento',)


#
# Admin para PrincipioAtivo
#
@admin.register(PrincipioAtivo)
class PrincipioAtivoAdmin(admin.ModelAdmin):
    list_display = (
        'idprincipio_ativo',
        'nome_principio_ativo',
    )
    search_fields = ('nome_principio_ativo',)
    ordering = ('nome_principio_ativo',)


#
# Admin para Laboratorio
#
@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = (
        'idlaboratorio',
        'nome_laboratorio',
    )
    search_fields = ('nome_laboratorio',)
    ordering = ('nome_laboratorio',)


#
# Admin para Doenca
#
@admin.register(Doenca)
class DoencaAdmin(admin.ModelAdmin):
    list_display = (
        'iddoenca',
        'nome_doenca',
    )
    search_fields = ('nome_doenca',)
    ordering = ('nome_doenca',)


#
# Admin para ResponsavelTecnico
#
@admin.register(ResponsavelTecnico)
class ResponsavelTecnicoAdmin(admin.ModelAdmin):
    list_display = (
        'idresponsavel_tecnico',
        'nome_responsavel',
    )
    search_fields = ('nome_responsavel',)
    ordering = ('nome_responsavel',)
