from rest_framework import serializers


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



