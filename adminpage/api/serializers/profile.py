from rest_framework import serializers


class IsIllSerializer(serializers.Serializer):
    is_ill = serializers.BooleanField()


class TrainingHourSerializer(serializers.Serializer):
    group = serializers.CharField()
    timestamp = serializers.DateTimeField()
    hours = serializers.FloatField()
