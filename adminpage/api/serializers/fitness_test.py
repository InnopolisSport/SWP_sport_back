from rest_framework import serializers

from api.serializers.semester import SemesterSerializer
from sport.models import FitnessTestExercise


class ExerciseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='exercise_name')
    semester = SemesterSerializer()
    unit = serializers.CharField(source='value_unit')
    select = serializers.ListSerializer(child=serializers.CharField())

    def set_select(self, x):
        return x.split(',')

    class Meta:
        model = FitnessTestExercise
        fields = ('id', 'semester', 'name', 'unit', 'select')


class ExercisesSerializer(serializers.ListSerializer):
    child = ExerciseSerializer()


class FitnessTestResult(serializers.Serializer):
    student_id = serializers.IntegerField()
    exercise_name = serializers.CharField()
    value = serializers.IntegerField()


class FitnessTestDetail(serializers.Serializer):
    exercise = serializers.CharField()
    unit = serializers.CharField(allow_null=True)
    value = serializers.Field()
    score = serializers.IntegerField()
    max_score = serializers.IntegerField()


class FitnessTestStudentResult(serializers.Serializer):
    semester = serializers.CharField()
    grade = serializers.BooleanField()
    total_score = serializers.IntegerField()
    details = FitnessTestDetail(many=True)


class FitnessTestStudentResults(serializers.ListSerializer):
    child = FitnessTestStudentResult()


class FitnessTestResults(serializers.Serializer):
    result = FitnessTestResult(many=True)


class FitnessTestSession(serializers.Serializer):
    date = serializers.DateTimeField()
    teacher = serializers.CharField()


class FitnessTestSessionFull(FitnessTestSession):
    results = FitnessTestResult(many=True)


class FitnessTestSessions(serializers.Serializer):
    session = FitnessTestSession(many=True)



