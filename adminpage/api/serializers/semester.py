from rest_framework import serializers
from sport.models import Semester


class SemesterInSerializer(serializers.Serializer):
    semester_id = serializers.IntegerField(required=False)


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('id', 'name')
