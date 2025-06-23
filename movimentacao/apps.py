from django.apps import AppConfig

class MovimentacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movimentacao'

    def ready(self):
        import movimentacao.signals
