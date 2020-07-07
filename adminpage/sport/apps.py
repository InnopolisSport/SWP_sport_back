from django.apps import AppConfig


class SportConfig(AppConfig):
    name = 'sport'

    def ready(self) -> None:
        from sport.models import MedicalGroup, medical_groups_name, medical_groups_description
        try:
            for medical_group in MedicalGroup.objects.all():
                medical_groups_name[medical_group.pk] = medical_group.name
                medical_groups_description[medical_group.pk] = medical_group.description
        except:
            pass
        import sport.signals  # noqa
        # TODO: resolve in a better way
        # if the database doesn't have a migration
        # on Group, these changes will cause an error
        # preventing database migration
        try:
            sport.signals.get_or_create_trainer_group()
            sport.signals.get_or_create_student_group()
        except:
            pass
