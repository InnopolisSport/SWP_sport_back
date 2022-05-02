from .attendance import (
    SuggestionQuerySerializer,
    SuggestionSerializer,
    StudentInfoSerializer,
    GradeReportSerializer,
    TrainingGradesSerializer,
    LastAttendedStat,
    LastAttendedDatesSerializer,
    BadGradeReportGradeSerializer,
    BadGradeReport,
    AttendanceMarkSerializer,
    HoursInfoSerializer,
    HoursInfoFullSerializer
)
from .calendar import (
    CalendarRequestSerializer,
    ScheduleExtendedPropsSerializer,
    CalendarSerializer,
)
from .common import (
    EmptySerializer,
    NotFoundSerializer,
    ErrorSerializer,
    InbuiltErrorSerializer,
    get_error_serializer,
    error_detail,
)
from .enroll import (
    EnrollSerializer,
    UnenrollStudentSerializer,
)
from .group import (
    ScheduleSerializer,
    SportSerializer,
    SportsSerializer,
    GroupInfoSerializer,
)
from .profile import (
    HasQRSerializer,
    TrainingHourSerializer,
)
from .reference import (
    ReferenceUploadSerializer,
)
from .self_sport_report import (
    SelfSportReportUploadSerializer,
)
from .tmp import (
    TmpSerializer,
)
from .training import (
    TrainingInfoSerializer,
)
from .fitness_test import (
    FitnessTestResult,
    FitnessTestResults
)
from .measurement import (
    Measurement,
    MeasurementResult
)
