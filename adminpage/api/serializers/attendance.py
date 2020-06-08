from rest_framework import serializers


class SuggestionQuerySerializer(serializers.Serializer):
    term = serializers.CharField()


class SuggestionSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class GradeReportSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    hours = serializers.FloatField(default=None)


class TrainingGradesSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    start = serializers.DateTimeField()
    grades = GradeReportSerializer(many=True)


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
