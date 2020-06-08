from django.apps import AppConfig


class SportConfig(AppConfig):
    name = 'sport'

    def ready(self) -> None:
        import sport.signals  # noqa
        sport.signals.get_or_create_trainer_group()
        sport.signals.get_or_create_student_group()
