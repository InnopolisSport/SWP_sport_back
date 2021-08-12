from django.db import models

from sport.models import Semester

from django.db.models import DecimalField, Sum, Q
from django.db.models.expressions import Subquery, OuterRef, ExpressionWrapper, F
from django.db.models.functions import Coalesce


def get_ongoing_semester() -> Semester:
    """
    Retrieves current ongoing semester
    @return ongoing semester
    """
    return Semester.objects.raw('SELECT * FROM semester WHERE id = current_semester()')[0]


class StudentHoursManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()

        # Get all hours for ongoing semester
        qs = qs.annotate(ongoing_semester_hours=Coalesce(Sum("attendance__hours",
                                                filter=Q(attendance__student=F("pk")) &
                                                       Q(attendance__training__group__semester=get_ongoing_semester())), 0))

        # To get previous semesters for current student exclude: (see comments below)
        previous_semesters_for_current_student = (
            Semester.objects
                .filter(end__lt=get_ongoing_semester().start)  # ongoing semester;
                .exclude(academic_leave_students=OuterRef("pk"))  # academic-leave semesters for current student;
                .exclude(end__year__lt=OuterRef("enrollment_year"))  # semesters, which current student wasn't enrolled.
        )

        # Get debt from previous semesters
        qs = qs.annotate(debt=Coalesce(Subquery(
            # TODO: Analyse answer https://stackoverflow.com/a/43771738 and complexity
            previous_semesters_for_current_student
                .values('hours').annotate(sum_hours=Sum('hours')).values('sum_hours')
        ), 0))

        # Get all hours for previous semesters
        qs = qs.annotate(last_semesters_hours=Coalesce(Sum("attendance__hours",
                                                        filter=Q(attendance__student=F("pk")) &
                                                               Q(attendance__training__group__semester__in=Subquery(previous_semesters_for_current_student.values('id')))), 0))

        qs = qs.annotate(complex_hours=ExpressionWrapper(F('ongoing_semester_hours') + F('last_semesters_hours') - F('debt'), output_field=DecimalField()))
        # print(qs.query)
        # print(qs.values())
        return qs