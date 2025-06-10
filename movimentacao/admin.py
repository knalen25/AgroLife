from django.contrib import admin
from .models import Movimentacao, StatusMovimentacao

@admin.register(StatusMovimentacao)
class StatusMovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('idstatus_movimentacao', 'nome_status')
    search_fields = ('nome_status',)

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('idmovimentacao', 'data_movimentacao', 'status', 'lote_origem', 'lote_destino', 'curral_destino')
    list_filter = ('status', 'lote_origem', 'lote_destino', 'curral_destino')
    search_fields = ('idmovimentacao',)
