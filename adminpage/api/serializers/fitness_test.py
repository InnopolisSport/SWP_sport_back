from rest_framework import serializers


class FitnessTestResult(serializers.Serializer):
    student_id = serializers.IntegerField()
    exercise_name = serializers.CharField()
    value = serializers.IntegerField()


class FitnessTestResults(serializers.Serializer):
    result = FitnessTestResult(many=True)
