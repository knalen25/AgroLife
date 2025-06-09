from django.contrib import admin
from .models import Lote # Importa o modelo Lote

# Registra o modelo Lote no admin
@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista do admin
    list_display = (
        'idlote',
        'nome_lote',
        'data_inicio_lote',
        'ativo',
        'curral', # Exibe o objeto Curral relacionado
    )
    # Campos que podem ser usados para pesquisa
    search_fields = (
        'nome_lote',
        'curral__nome_curral', # Permite pesquisar lotes pelo nome do curral ao qual estão vinculados
    )
    # Filtros na barra lateral direita do admin
    list_filter = (
        'ativo',
        'curral', # Permite filtrar por curral
        'data_inicio_lote', # Permite filtrar por data de início do lote
    )
    # Campos para ordenação padrão
    ordering = (
        'nome_lote',
        'data_inicio_lote',
    )
    # raw_id_fields = ('curral',) # Opcional: use para melhorar o desempenho em casos com muitos currais
