from django.apps import AppConfig


class Accounts1Config(AppConfig):
    name = 'accounts1'

    def ready(self):
        import  accounts1.signals
