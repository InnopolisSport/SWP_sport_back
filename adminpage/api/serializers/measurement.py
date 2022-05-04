from rest_framework import serializers


class Measurement(serializers.Serializer):
    name = serializers.CharField()
    value_unit = serializers.CharField()


class MeasurementPost(serializers.Serializer):
    student_id = serializers.IntegerField()
    measurement_id = serializers.IntegerField()
    value = serializers.IntegerField()


class MeasurementResult(serializers.Serializer):
    measurement = serializers.CharField()
    uint = serializers.CharField()
    value = serializers.IntegerField()
    approved = serializers.BooleanField()
    date = serializers.DateField()


class MeasurementResults(serializers.Serializer):
    semester = serializers.CharField()
    result = MeasurementResult(many=True)
