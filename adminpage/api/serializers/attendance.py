from rest_framework import serializers


class SuggestionQuerySerializer(serializers.Serializer):
    term = serializers.CharField()
    group_id = serializers.IntegerField()


class SuggestionSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class StudentInfoSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()


class GradeReportSerializer(StudentInfoSerializer):
    hours = serializers.FloatField(default=None)


class TrainingGradesSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    start = serializers.DateTimeField()
    grades = GradeReportSerializer(many=True)


class LastAttendedStat(StudentInfoSerializer):
    last_attended = serializers.CharField()


class LastAttendedDatesSerializer(serializers.Serializer):
    last_attended_dates = LastAttendedStat(many=True)


class BadGradeReportGradeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    hours = serializers.FloatField()


class BadGradeReport(serializers.Serializer):
    code = serializers.IntegerField()
    description = serializers.CharField()
    negative_marks = BadGradeReportGradeSerializer(many=True, default=None)
    overflow_marks = BadGradeReportGradeSerializer(many=True, default=None)


class GradeSetSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    hours = serializers.FloatField()


class AttendanceMarkSerializer(serializers.Serializer):
    training_id = serializers.IntegerField()
    students_hours = GradeSetSerializer(many=True)


class HourInfoSemesterChildSerializer(serializers.Serializer):
    id_sem = serializers.IntegerField()
    hours_not_self_current = serializers.FloatField()
    hours_self_not_debt_current = serializers.FloatField()
    hours_self_debt_current = serializers.FloatField()
    hours_sem_max_current = serializers.FloatField()


class HoursInfoSerializer(serializers.Serializer):
    last_semesters_hours = HourInfoSemesterChildSerializer(many=True)
    ongoing_semester = HourInfoSemesterChildSerializer()

