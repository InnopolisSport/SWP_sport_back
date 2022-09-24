from rest_framework import serializers

from sport.models import Sport


class NewSportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name', 'description')
