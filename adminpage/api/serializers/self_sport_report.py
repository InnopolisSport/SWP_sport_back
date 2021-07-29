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
    debt = serializers.BooleanField(required=True)
    # start = serializers.DateTimeField(required=True)
    # end = serializers.DateTimeField(required=True)
    hours = serializers.IntegerField()

    class Meta:
        model = SelfSportReport
        fields = (
            'link',
            'hours',
            'training_type',
            'debt'
        )
