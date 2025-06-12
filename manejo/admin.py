from django.contrib import admin
from .models import (
    Manejo,
    ParametroManejo,
    BoiManejo,
    StatusManejo,
)

class BoiManejoInline(admin.TabularInline):
    model = BoiManejo
    extra = 1
    autocomplete_fields = ('boi',)
    verbose_name = "Boi no Manejo"
    verbose_name_plural = "Bois no Manejo"

class ParametroManejoInline(admin.TabularInline):
    model = ParametroManejo
    extra = 1
    autocomplete_fields = ('lote', 'raca')
    fields = ('lote', 'raca', 'peso_inicial', 'peso_final')
    verbose_name = "Parâmetro de Manejo"
    verbose_name_plural = "Parâmetros de Manejo"


@admin.register(Manejo)
class ManejoAdmin(admin.ModelAdmin):
    list_display = (
        'idManejo',
        'data_manejo',
        'tipo_manejo',
        'status_manejo',
        'protocolo_sanitario',
    )
    list_filter = ('tipo_manejo', 'status_manejo', 'data_manejo')
    search_fields = ('idManejo', 'protocolo_sanitario__nome_protocolo')
    ordering = ('-data_manejo',)
    autocomplete_fields = ('status_manejo', 'protocolo_sanitario')
    inlines = [ParametroManejoInline, BoiManejoInline]

@admin.register(BoiManejo)
class BoiManejoAdmin(admin.ModelAdmin):
    list_display = ('idboi_manejo', 'boi', 'manejo', 'protocolo_sanitario')
    autocomplete_fields = ('boi', 'manejo', 'protocolo_sanitario')
    search_fields = ('boi__brinco', 'manejo__idManejo')
    list_filter = ('protocolo_sanitario',)

@admin.register(StatusManejo)
class StatusManejoAdmin(admin.ModelAdmin):
    list_display = ('idstatus_manejo', 'nome_status_manejo')
    search_fields = ('nome_status_manejo',)
    ordering = ('nome_status_manejo',)
