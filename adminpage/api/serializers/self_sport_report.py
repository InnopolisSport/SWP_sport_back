from rest_framework import serializers

from sport.models import SelfSportReport, SelfSportType


class SelfSportTypes(serializers.ModelSerializer):
    class Meta:
        model = SelfSportType
        fields = (
            'pk',
            'name',
            'application_rule',
        )


class SelfSportReportUploadSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(allow_empty_file=False, required=False)
    link = serializers.URLField(required=True)
    training_type = serializers.PrimaryKeyRelatedField(
        queryset=SelfSportType.objects.filter(
            is_active=True,
        ).all()
    )
    # start = serializers.DateTimeField(required=True)
    # end = serializers.DateTimeField(required=True)
    hours = serializers.IntegerField()
    student_comment = serializers.CharField(required=False, allow_blank=True)
    parsed_data = serializers.JSONField(required=False)

    class Meta:
        model = SelfSportReport
        fields = (
            'link',
            'hours',
            'training_type',
            'student_comment',
            'parsed_data'
        )


class ActivitySerializer(serializers.Serializer):
    link = serializers.URLField(required=True)


class ParsedActivitySerializer(serializers.Serializer):
    training_type = serializers.CharField()
    avg_pace = serializers.CharField(required=False)  # Intended to be used by teachers
    avg_speed = serializers.CharField(required=False)  # Measured in km/h
    avg_heart_rate = serializers.CharField(required=False)  # Measured in bpm
    distance = serializers.IntegerField()  # Measured in km
    hours = serializers.IntegerField()
    approved = serializers.BooleanField()
