from rest_framework import serializers

from sport.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "weekday",
            "start",
            "end",
            "training_class",
        )

class SportEnrollSerializer(serializers.Serializer):
    sport_id = serializers.IntegerField()

class SportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    special = serializers.BooleanField()

class SportsSerializer(serializers.Serializer):
    sports = serializers.ListField(child=SportSerializer())


class TrainerSerializer(serializers.Serializer):
    trainer_first_name = serializers.CharField()
    trainer_last_name = serializers.CharField()
    trainer_email = serializers.CharField()


class GroupInfoSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    group_description = serializers.CharField()
    capacity = serializers.IntegerField()
    current_load = serializers.IntegerField()

    trainer_first_name = serializers.CharField()
    trainer_last_name = serializers.CharField()
    trainer_email = serializers.CharField()

    trainers = TrainerSerializer(many=True)

    link = serializers.URLField()
    link_name = serializers.CharField()

    is_enrolled = serializers.BooleanField()

    schedule = ScheduleSerializer(many=True)
