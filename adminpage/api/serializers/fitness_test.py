from rest_framework import serializers

from api.serializers.semester import SemesterSerializer
from api.serializers.student import StudentSerializer
from sport.models import FitnessTestExercise, FitnessTestSession, FitnessTestResult


class FitnessTestExerciseSelectSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        return ','.join(data)

    def to_representation(self, data):
        return data.split(',')


class FitnessTestExerciseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='exercise_name')
    semester = SemesterSerializer()
    unit = serializers.CharField(source='value_unit')
    select = FitnessTestExerciseSelectSerializer(child=serializers.CharField())

    class Meta:
        model = FitnessTestExercise
        fields = ('id', 'semester', 'name', 'unit', 'select')


class FitnessTestResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = FitnessTestResult
        fields = ('student', 'value')


class FitnessTestDetail(serializers.Serializer):
    exercise = serializers.CharField()
    unit = serializers.CharField(allow_null=True)
    value = serializers.Field()
    score = serializers.IntegerField()
    max_score = serializers.IntegerField()


class FitnessTestStudentResult(serializers.Serializer):
    semester = serializers.CharField()
    retake = serializers.BooleanField()
    grade = serializers.BooleanField()
    total_score = serializers.IntegerField()
    details = FitnessTestDetail(many=True)


class FitnessTestResults(serializers.Serializer):
    result = FitnessTestResultSerializer(many=True)

class FitnessTestResult(serializers.Serializer):
    student_id = serializers.IntegerField()
    exercise_id = serializers.IntegerField()
    value = serializers.CharField()


class FitnessTestUpload(serializers.Serializer):
    retake = serializers.BooleanField()
    results = serializers.ListField(child=FitnessTestResult())


class FitnessTestSessionSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    teacher = serializers.CharField(source='teacher.__str__')  # TODO: return object

    class Meta:
        model = FitnessTestSession
        fields = ('id', 'date', 'teacher', 'semester')


class FitnessTestSessionWithResult(serializers.Serializer):
    session = FitnessTestSessionSerializer()
    exercises = FitnessTestExerciseSerializer(many=True)
    results = serializers.DictField(child=FitnessTestResultSerializer(many=True))
