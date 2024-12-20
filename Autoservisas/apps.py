from django.apps import AppConfig


class AutoservisasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Autoservisas'

    def ready(self):
        from .signals import create_profile, save_profile