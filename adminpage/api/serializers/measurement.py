from rest_framework import serializers


class Measurement(serializers.Serializer):
    student_id = serializers.IntegerField()
    measurement_name = serializers.CharField()
    value = serializers.IntegerField()


class MeasurementSession(serializers.Serializer):
    student_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    semester_id = serializers.IntegerField()
    approved = serializers.BooleanField()


class MeasurementResult(serializers.Serializer):
    session_id = serializers.IntegerField()
    measurement_id = serializers.IntegerField()
    value = serializers.IntegerField()
