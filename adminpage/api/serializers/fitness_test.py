from rest_framework import serializers


class FitnessTestResult(serializers.Serializer):
    student_id = serializers.IntegerField()
    exercise_name = serializers.CharField()
    value = serializers.IntegerField()


class FitnessTestResults(serializers.Serializer):
    result = FitnessTestResult(many=True)


class FitnessTestSession(serializers.Serializer):
    date = serializers.DateTimeField()
    teacher = serializers.CharField()


class FitnessTestSessionFull(FitnessTestSession):
    results = FitnessTestResult(many=True)


class FitnessTestSessions(serializers.Serializer):
    session = FitnessTestSession(many=True)



