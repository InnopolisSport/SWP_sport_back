from adminpage.swagger import schema_view
from django.urls import path, re_path, register_converter

from api.views import (
    tmp,
    profile,
    enroll,
    group,
    training,
    attendance,
    calendar,
    reference,
    self_sport_report,
)

class NegativeIntConverter:
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value

register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path(r"test/", tmp.test),
    # profile
    path(r"profile/sick/toggle", profile.toggle_sick),
    path(r"profile/history/<int:semester_id>", profile.get_history),
    path(r"profile/history_with_self/<int:semester_id>", profile.get_history_with_self),

    # enroll
    path(r"enrollment/enroll", enroll.enroll),
    path(r"enrollment/unenroll", enroll.unenroll),
    path(r"enrollment/unenroll_by_trainer", enroll.unenroll_by_trainer),

    # group
    path(r"group/<int:group_id>", group.group_info_view),
    path(r"select_sport", group.select_sport),
    path(r"sports", group.sports_view),

    # training
    path(r"training/<int:training_id>", training.training_info),

    # attendance
    path(r"attendance/suggest_student", attendance.suggest_student),
    path(r"attendance/<int:training_id>/grades", attendance.get_grades),
    path(r"attendance/<int:group_id>/report",
         attendance.get_last_attended_dates),
    path(r"attendance/mark", attendance.mark_attendance),
    path(r"attendance/<int:student_id>/hours", attendance.get_student_hours_info),
    path(r"attendance/<int:student_id>/negative_hours", attendance.get_negative_hours_info),

    # calendar
    path(r"calendar/<negint:sport_id>/schedule", calendar.get_schedule),
    path(r"calendar/trainings", calendar.get_personal_schedule),

    # reference management
    path(r"reference/upload", reference.reference_upload),

    # self sport report
    path(r"selfsport/upload", self_sport_report.self_sport_upload),
    path(r"selfsport/types", self_sport_report.get_self_sport_types),
    path(r"selfsport/strava_parsing", self_sport_report.get_strava_activity_info)
]

urlpatterns.extend([
    re_path(
        r'swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
])
