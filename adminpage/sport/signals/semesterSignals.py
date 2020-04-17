from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from sport.models import Semester, Sport, Trainer, Group


@receiver(post_save, sender=Semester)
def special_groups_create(sender, instance, created, **kwargs):
    if created:
        # get_or_create returns (object: Model, created: bool)
        other_sport, _ = Sport.objects.get_or_create(name="Other", special=True)
        sport_dep, _ = Trainer.objects.get_or_create(first_name="Sport", last_name="Department",
                                                     email=settings.SPORT_DEPARTMENT_EMAIL)
        trainer_group = Group(name="SC trainers", capacity=9999,
                              is_club=False, sport=other_sport,
                              semester=instance,
                              trainer=sport_dep)
        trainer_group.save()
        sport_event_group = Group(name="Extra sport events", capacity=9999,
                                  is_club=False, sport=other_sport,
                                  semester=instance,
                                  trainer=sport_dep)
        sport_event_group.save()
