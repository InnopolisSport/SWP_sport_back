from .attendance import *
from .enroll import *
from .group import *
from .schedule import *
from .semester import *
from .sport import *
from .student import *
from .trainer import *
from .training import *
from .training_class import *

from django.contrib.auth.models import Group as DjangoGroup
DjangoGroup.add_to_class(
    'verbose_name', 
    models.CharField(
        max_length=180,
        null=True, blank=False,
        unique=True,
        )
    )
