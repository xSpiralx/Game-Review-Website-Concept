from django.apps import AppConfig


class Demo1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demo1'

class Demo1Config(AppConfig):
    name = 'demo1'

    def ready(self):
        import demo1.signals

