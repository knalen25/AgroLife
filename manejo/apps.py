from django.apps import AppConfig

class ManejoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manejo'

    def ready(self):
        import manejo.signals