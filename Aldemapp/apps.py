from django.apps import AppConfig


class AldemappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aldemapp'
    verbose_name = "أ.الدمرداش"
    
    def ready(self):
        import Aldemapp.signals
    
