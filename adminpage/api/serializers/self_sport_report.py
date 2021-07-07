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
    link = serializers.URLField(required=False)
    training_type = serializers.PrimaryKeyRelatedField(
        queryset=SelfSportType.objects.filter(
            is_active=True,
        ).all()
    )
    # start = serializers.DateTimeField(required=True)
    # end = serializers.DateTimeField(required=True)

    def validate(self, data):
        # image_present = 'image' in data
        link_present = 'link' in data
        # if (image_present and link_present) or \
        #         (not image_present and not link_present):
        #     raise serializers.ValidationError(
        #         "Must include either image or link"
        #     )
        if (not link_present):
            raise serializers.ValidationError(
                "Must include a link to Strava activity"
            )
        return data

    class Meta:
        model = SelfSportReport
        fields = (
            'image',
            'link',
            # 'start',
            # 'end',
            'training_type',
        )
