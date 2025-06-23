from django.contrib import admin
from .models import Lote

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = (
        'idlote',
        'nome_lote',
        'data_inicio_lote',
        'ativo',
        'curral',
    )
    search_fields = (
        'nome_lote',
        'curral__nome_curral',
    )
    list_filter = (
        'ativo',
        'curral',
        'data_inicio_lote',
    )
    ordering = (
        'nome_lote',
        'data_inicio_lote',
    )
