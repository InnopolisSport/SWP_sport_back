from rest_framework import serializers


class TmpSerializer(serializers.Serializer):
    ping = serializers.CharField()
