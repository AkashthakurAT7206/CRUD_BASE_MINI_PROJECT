from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    
    def ready(self):
        # Import signal handlers
        from . import signals  # noqa: F401