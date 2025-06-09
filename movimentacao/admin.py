from django.contrib import admin
from .models import (
    StatusMovimentacao,
    Movimentacao,
    MovimentacaoLoteOrigem,
    MovimentacaoLoteDestino
)


class MovimentacaoLoteOrigemInline(admin.TabularInline):
    model = MovimentacaoLoteOrigem
    extra = 1
    fields = ("curral", "lote")
    verbose_name = "Origem de Lote"
    verbose_name_plural = "Lotes de Origem"


class MovimentacaoLoteDestinoInline(admin.TabularInline):
    model = MovimentacaoLoteDestino
    extra = 1
    fields = ("lote", "curral")
    verbose_name = "Destino de Lote"
    verbose_name_plural = "Lotes de Destino"


@admin.register(StatusMovimentacao)
class StatusMovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("idstatus_movimentacao", "nome_status")
    search_fields = ("nome_status",)
    ordering = ("nome_status",)
    list_per_page = 20


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("idmovimentacao", "data_movimentacao", "status")
    list_filter = ("status", "data_movimentacao")
    search_fields = ("idmovimentacao", "status__nome_status")
    ordering = ("-data_movimentacao",)
    date_hierarchy = "data_movimentacao"
    fieldsets = (
        (
            "Dados da Movimentação",
            {
                "fields": ("data_movimentacao", "status"),
            },
        ),
    )
    inlines = [MovimentacaoLoteOrigemInline, MovimentacaoLoteDestinoInline]


@admin.register(MovimentacaoLoteOrigem)
class MovimentacaoLoteOrigemAdmin(admin.ModelAdmin):
    list_display = ("idmovimentacao_lote_origem", "movimentacao", "curral", "lote")
    list_filter = ("curral", "lote", "movimentacao__status")
    search_fields = (
        "movimentacao__idmovimentacao",
        "curral__nome_curral",
        "lote__nome_lote",
    )
    ordering = ("movimentacao__data_movimentacao",)
    date_hierarchy = "movimentacao__data_movimentacao"
    fieldsets = (
        (
            "Origem de Lote na Movimentação",
            {
                "fields": ("movimentacao", "curral", "lote"),
            },
        ),
    )


@admin.register(MovimentacaoLoteDestino)
class MovimentacaoLoteDestinoAdmin(admin.ModelAdmin):
    list_display = ("idmovimentacao_lote_destino", "movimentacao", "lote", "curral")
    list_filter = ("lote", "curral", "movimentacao__status")
    search_fields = (
        "movimentacao__idmovimentacao",
        "lote__nome_lote",
        "curral__nome_curral",
    )
    ordering = ("movimentacao__data_movimentacao",)
    date_hierarchy = "movimentacao__data_movimentacao"
    fieldsets = (
        (
            "Destino de Lote na Movimentação",
            {
                "fields": ("movimentacao", "lote", "curral"),
            },
        ),
    )