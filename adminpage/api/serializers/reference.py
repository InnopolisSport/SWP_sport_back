from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sport.models import Reference


class ReferenceUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=False)

    def validate_image(self, image):
        if image.size > settings.MAX_IMAGE_SIZE:
            raise ValidationError("Image file size too big")
        width, height = image.image.size
        if width > settings.MAX_IMAGE_DIMENSION \
                or width < settings.MIN_IMAGE_DIMENSION \
                or height > settings.MAX_IMAGE_DIMENSION \
                or height < settings.MIN_IMAGE_DIMENSION:
            raise ValidationError(
                f"Invalid image width/height, expected them to be in range {settings.MIN_IMAGE_DIMENSION}..{settings.MAX_IMAGE_DIMENSION}"
            )
        return image

    class Meta:
        model = Reference
        fields = ['image']
