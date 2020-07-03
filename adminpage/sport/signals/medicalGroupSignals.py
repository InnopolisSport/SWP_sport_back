from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from sport.models import medical_groups_name, medical_groups_description, MedicalGroup


@receiver(post_save, sender=MedicalGroup)
def update_medical_groups(instance: MedicalGroup, created, **kwargs):
    medical_groups_name.clear()
    medical_groups_description.clear()
    for medical_group in MedicalGroup.objects.all():
        medical_groups_name[medical_group.pk] = medical_group.name
        medical_groups_description[medical_group.pk] = medical_group.description
