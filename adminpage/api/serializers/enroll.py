from rest_framework import serializers


class EnrollSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
