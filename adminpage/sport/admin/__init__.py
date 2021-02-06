from django.contrib import admin

# add save button on top for all admins
admin.ModelAdmin.save_on_top = True

from .site import SportAdminSite, site
from .userAdmin import UserAdmin
from .enrollAdmin import EnrollAdmin
from .trainerAdmin import TrainerAdmin
from .sportAdmin import SportAdmin
from .trainingAdmin import TrainingAdmin
from .groupAdmin import GroupAdmin
from .attendanceAdmin import AttendanceAdmin
from .scheduleAdmin import ScheduleAdmin
from .selfSportAdmin import SelfSportAdmin
from .selfsportTypeAdmin import SelfSportTypeAdmin
from .semesterAdmin import SemesterAdmin
from .studentAdmin import StudentAdmin
from .studentMedicalGroupAdmin import StudentMedicalGroupAdmin
from .trainingClassAdmin import TrainingClassAdmin
from .djangoGroupAdmin import DjangoGroupAdmin
from .referenceAdmin import ReferenceAdmin
from .medicalGroupAdmin import MedicalGroupAdmin
from .medicalGroupReferenceAdmin import MedicalGroupReferenceAdmin
