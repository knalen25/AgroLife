from django.contrib import admin
from .models import TipoCurral, Curral

@admin.register(TipoCurral)
class TipoCurralAdmin(admin.ModelAdmin):
    list_display = (
        'idTipo_curral',
        'nome_tipo_curral',
    )
    search_fields = (
        'nome_tipo_curral',
    )
    ordering = ('nome_tipo_curral',)

@admin.register(Curral)
class CurralAdmin(admin.ModelAdmin):
    list_display = (
        'idCurral',
        'nome_curral',
        'peso_min',
        'peso_max',
        'area_m2',
        'area_coche',
        'ativo',
        'tipo_curral',
    )
    search_fields = (
        'nome_curral',
    )
    list_filter = (
        'ativo',
        'tipo_curral',
    )
    ordering = (
        'nome_curral',
        'idCurral'
    )