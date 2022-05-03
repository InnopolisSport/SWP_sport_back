from rest_framework import serializers


class Measurement(serializers.Serializer):
    student_id = serializers.IntegerField()
    measurement_name = serializers.CharField()
    value = serializers.IntegerField()


class MeasurementResult(serializers.Serializer):
    measurement = serializers.CharField()
    uint = serializers.CharField()
    value = serializers.IntegerField()
    approved = serializers.BooleanField()
    date = serializers.DateField()
    semester = serializers.CharField()


class MeasurementResults(serializers.Serializer):
    results = MeasurementResult(many=True)
