from rest_framework import serializers

from sport.models import SelfSportReport


class SelfSportReportUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=False, required=False)
    link = serializers.URLField(required=False)

    def validate(self, data):
        image_present = 'image' in data
        link_present = 'link' in data
        if (image_present and link_present) or \
                (not image_present and not link_present):
            raise serializers.ValidationError(
                "Must include either image or link"
            )
        return data

    class Meta:
        model = SelfSportReport
        fields = ('image', 'link')
