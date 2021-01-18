from rest_framework import serializers


class TrainingInfoSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    group_description = serializers.CharField()

    training_class = serializers.CharField(default=None)

    capacity = serializers.IntegerField()
    current_load = serializers.IntegerField()

    trainer_first_name = serializers.CharField()
    trainer_last_name = serializers.CharField()
    trainer_email = serializers.CharField()

    hours = serializers.FloatField(default=None)

    is_enrolled = serializers.BooleanField()
