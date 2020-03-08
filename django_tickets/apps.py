from django.apps import AppConfig


class DjangoTicketsConfig(AppConfig):
    name = 'django_tickets'

    def ready(self, *args, **kwargs):
        import django_tickets.signals
        print('ready worked')
