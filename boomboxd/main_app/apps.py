from django.apps import AppConfig
from django.db.models.signals import post_save



class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    # add this
    def ready(self):
        import boomboxd.main_app.signals


