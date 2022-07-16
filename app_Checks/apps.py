from django.apps import AppConfig


class AppChecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_Checks'
    verbose_name = 'چک'
    verbose_name_plural = f'{verbose_name} ها'
