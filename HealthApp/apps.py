from django.apps import AppConfig


class HealthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HealthApp'

    def ready(self):
        import HealthApp.signals  # Make sure the app name is correct

