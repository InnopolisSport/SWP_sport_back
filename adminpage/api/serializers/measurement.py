from rest_framework import serializers

class Measurement(serializers.Serializer):
    student_id = serializers.IntegerField()
    measurement_name = serializers.CharField()
    value = serializers.IntegerField()
