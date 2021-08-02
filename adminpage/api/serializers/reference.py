from rest_framework import serializers

from sport.models import Reference


class ReferenceUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=False)
    start = serializers.DateField(allow_null=False)
    end = serializers.DateField(allow_null=False)
    student_comment = serializers.CharField(max_length=1024, allow_null=True)

    class Meta:
        model = Reference
        fields = ['image', 'start', 'end', 'student_comment']
