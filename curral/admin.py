from django.contrib import admin
from .models import TipoCurral, Curral

# Registra o modelo TipoCurral no admin
@admin.register(TipoCurral)
class TipoCurralAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista do admin
    list_display = (
        'idTipo_curral',
        'nome_tipo_curral',
    )
    # Campos que podem ser usados para pesquisa
    search_fields = (
        'nome_tipo_curral',
    )
    # Ordenação padrão da lista
    ordering = ('nome_tipo_curral',)


# Registra o modelo Curral no admin
@admin.register(Curral)
class CurralAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista do admin
    list_display = (
        'idCurral',
        'nome_curral',
        'peso_min',
        'peso_max',
        'area_m2',
        'area_coche',
        'ativo',
        'tipo_curral', # Exibe o objeto TipoCurral relacionado
    )
    # Campos que podem ser usados para pesquisa
    search_fields = (
        'nome_curral',
    )
    # Filtros na barra lateral direita do admin
    list_filter = (
        'ativo',
        'tipo_curral', # Permite filtrar por tipo de curral
    )
    # Campos para ordenação padrão
    ordering = (
        'nome_curral',
        'idCurral'
    )