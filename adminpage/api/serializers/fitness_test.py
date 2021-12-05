from rest_framework import serializers


class FitnessTestResult(serializers.Serializer):
    exercise_name = serializers.CharField()
    value = serializers.IntegerField()


class FitnessTestResults(serializers.Serializer):
    student_email = serializers.CharField()
    result = FitnessTestResult(many=True)
