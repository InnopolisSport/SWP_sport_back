from .attendance import *
from .enroll import *
from .group import *
from .medical_group import *
from .schedule import *
from .semester import *
from .sport import *
from .student import *
from .trainer import *
from .training import *
from .training_class import *
from .reference import *
from .enums import *

from django.contrib.auth.models import Group as DjangoGroup
DjangoGroup.add_to_class(
    'verbose_name',
    models.CharField(
        max_length=180,
        null=True, blank=False,
        unique=True,
        )
    )

DjangoGroup.add_to_class(
    "__str__",
    lambda self: str(self.verbose_name)
)

DjangoGroup.add_to_class(
    "natural_key",
    lambda self: (str(self.verbose_name), )
)
