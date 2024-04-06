from django.apps import AppConfig


class NonAuthenticatedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'non_authenticated'
