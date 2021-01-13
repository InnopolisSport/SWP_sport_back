from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# add save button on top for all admins
admin.ModelAdmin.save_on_top = True

from .site import SportAdminSite, site
from .enrollAdmin import EnrollAdmin
from .trainerAdmin import TrainerAdmin
from .sportAdmin import SportAdmin
from .trainingAdmin import TrainingAdmin
from .groupAdmin import GroupAdmin
from .attendanceAdmin import AttendanceAdmin
from .scheduleAdmin import ScheduleAdmin
from .semesterAdmin import SemesterAdmin
from .studentAdmin import StudentAdmin
from .trainingClassAdmin import TrainingClassAdmin
from .djangoGroupAdmin import DjangoGroupAdmin
from .referenceAdmin import ReferenceAdmin
from .medicalGroupAdmin import MedicalGroupAdmin
from .medicalGroupReferenceAdmin import MedicalGroupReferenceAdmin

site.register(User, UserAdmin)
