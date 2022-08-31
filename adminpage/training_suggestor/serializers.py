from rest_framework import serializers

from training_suggestor.models import ExerciseParams, Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseParamsSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = ExerciseParams
        fields = ('exercise', 'type', 'power_zone', 'repeat', 'set', 'working_time', 'full_time', 'working_load')


class TrainingSerializer(serializers.Serializer):
    exercises = ExerciseParamsSerializer(many=True)
