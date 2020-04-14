from django.apps import AppConfig


class SportConfig(AppConfig):
    name = 'sport'

    def ready(self) -> None:
        pass
