from django.contrib import admin
from .models import (
    Fornecedor,
    Sexo,
    Raca,
    StatusBoi,
    Boi,
    PesoMovimentacao,
    PesoProjetado,
)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("idfornecedor", "nome_fornecedor")
    search_fields = ("nome_fornecedor",)
    ordering = ("nome_fornecedor",)
    list_per_page = 20

@admin.register(Sexo)
class SexoAdmin(admin.ModelAdmin):
    list_display = ("idsexo", "tipo_sexo")
    search_fields = ("tipo_sexo",)
    ordering = ("tipo_sexo",)
    list_per_page = 20

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ("idraca", "nome_raca")
    search_fields = ("nome_raca",)
    ordering = ("nome_raca",)
    list_per_page = 20

@admin.register(StatusBoi)
class StatusBoiAdmin(admin.ModelAdmin):
    list_display = ("idstatus_boi", "nome_status")
    search_fields = ("nome_status",)
    ordering = ("nome_status",)
    list_per_page = 20

@admin.register(Boi)
class BoiAdmin(admin.ModelAdmin):
    list_display = (
        "idboi",
        "brinco",
        "sexo",
        "raca",
        "status_boi",
        "lote",
        "data_entrada",
        "data_saida",
    )
    list_filter = ("sexo", "raca", "status_boi", "lote")
    search_fields = ("brinco", "chip")
    ordering = ("brinco",)
    date_hierarchy = "data_entrada"
    fieldsets = (
        (
            "Identificação",
            {
                "fields": (
                    "brinco",
                    "chip",
                    "sexo",
                    "raca",
                    "fornecedor",
                    "lote",
                    "status_boi",
                )
            },
        ),
        (
            "Pesos e Datas",
            {
                "fields": (
                    "peso_entrada",
                    "peso_saida",
                    "data_nascimento",
                    "data_entrada",
                    "data_saida",
                    "data_morte",
                )
            },
        ),
        (
            "Informações Adicionais",
            {
                "fields": ("motivo_morte", "necropsia"),
            },
        ),
    )

@admin.register(PesoMovimentacao)
class PesoMovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("id_peso_movimentacao", "boi", "data_movimentacao", "peso_movimentacao")
    list_filter = ("boi", "data_movimentacao")
    search_fields = ("boi__brinco",)
    ordering = ("-data_movimentacao",)
    date_hierarchy = "data_movimentacao"
    fieldsets = (
        (
            "Registro de Pesagem",
            {
                "fields": ("boi", "data_movimentacao", "peso_movimentacao"),
            },
        ),
    )

@admin.register(PesoProjetado)
class PesoProjetadoAdmin(admin.ModelAdmin):
    list_display = ("id_peso_projetado", "boi", "data_projetado", "peso_projetado")
    list_filter = ("boi", "data_projetado")
    search_fields = ("boi__brinco",)
    ordering = ("data_projetado",)
    date_hierarchy = "data_projetado"
    fieldsets = (
        (
            "Registro de Projeção de Peso",
            {
                "fields": ("boi", "data_projetado", "peso_projetado"),
            },
        ),
    )