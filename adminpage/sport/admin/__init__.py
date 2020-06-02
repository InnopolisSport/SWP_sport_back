from django.contrib import admin
# add save button on top for all admins
admin.ModelAdmin.save_on_top = True

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
