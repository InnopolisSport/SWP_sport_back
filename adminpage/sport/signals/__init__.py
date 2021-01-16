from .schedule import (
    remove_future_trainings_from_schedule,
    create_trainings_current_semester,
)
from .semester import (
    special_groups_create,
    get_or_create_student_group,
)
from .user import (
    create_student_profile,
    verify_bachelor_role,
)
from .reference import update_hours_for_reference
from .self_sport_report import update_attendance_record
