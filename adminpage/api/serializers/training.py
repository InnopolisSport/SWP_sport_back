from rest_framework import serializers

from api.serializers.semester import SemesterSerializer
from sport.models import Training, Group, Trainer


class NewTrainerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email')


class NewGroupSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    teachers = NewTrainerSerializer(source='trainers', many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'link_name', 'link', 'capacity', 'is_club', 'sport', 'semester', 'teachers')


class NewTrainingInfoSerializer(serializers.ModelSerializer):
    group = NewGroupSerializer()
    load = serializers.SerializerMethodField()

    def get_load(self, obj: Training) -> int:
        return obj.checkins.count()

    class Meta:
        model = Training
        fields = ('id', 'group', 'start', 'end', 'load')

class NewTrainingInfoStudentSerializer(serializers.Serializer):
    training = NewTrainingInfoSerializer()
    can_check_in = serializers.BooleanField()
    checked_in = serializers.BooleanField()


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

    hours = serializers.IntegerField(default=None)

    is_enrolled = serializers.BooleanField()
