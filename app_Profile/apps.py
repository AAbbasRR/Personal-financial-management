from django.apps import AppConfig


class AppProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_Profile'
    verbose_name = 'حساب'
    verbose_name_plural = 'حساب ها'

    def ready(self):
        import app_Profile.signals
