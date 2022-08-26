from django.db import models


class ExerciseTypeChoices(models.TextChoices):
    WARMUP = 'WU', 'Warmup'
    PRESET = 'PS', 'Preset'
    MAINSET = 'MS', 'Main set'
    COOLDOWN = 'CD', 'Cooldown'
