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


class GroupInfoSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    group_description = serializers.CharField()
    capacity = serializers.IntegerField()
    current_load = serializers.IntegerField()

    trainer_first_name = serializers.CharField()
    trainer_last_name = serializers.CharField()
    trainer_email = serializers.CharField()

    is_enrolled = serializers.BooleanField()

    schedule = ScheduleSerializer(many=True)
