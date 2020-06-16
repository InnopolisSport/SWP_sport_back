from rest_framework import serializers

from sport.models import Reference


class ReferenceUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=False)

    class Meta:
        model = Reference
        fields = ['image']
