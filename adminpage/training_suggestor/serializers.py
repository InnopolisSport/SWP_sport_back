from rest_framework import serializers
from training_suggestor.models import ExerciseParams, Exercise, Poll, PollQuestion, PollResult, PollAnswer


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


class PollQuestionAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()
    time_ratio_influence = serializers.FloatField()
    working_load_ratio_influence = serializers.FloatField()


class PollQuestionSerializer(serializers.ModelSerializer):
    answers = PollQuestionAnswerSerializer(many=True)
    class Meta:
        model = PollQuestion
        fields = ('id', 'state', 'question', 'answers')


class PollSerializer(serializers.ModelSerializer):
    questions = PollQuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('name', 'questions')


class PollAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollAnswer
        fields = ('question', 'answer')


class PollResultSerializer(serializers.ModelSerializer):
    answers = PollAnswerSerializer(many=True)
    poll = serializers.CharField(source='poll.name')

    def is_valid(self, raise_exception=False):
        base = super().is_valid(raise_exception)
        if base:
            self._poll = Poll.objects.get(name=self.validated_data['poll']['name'])
            questions = {e[0]: [a['answer'] for a in e[1]] for e in self._poll.questions.all().values_list('id', 'answers')}
            questions_ids = set(questions.keys())
            answers_ids = {a['question'].pk for a in self.validated_data['answers']}
            print(questions_ids, answers_ids)
            if questions_ids != answers_ids:
                if questions_ids.issuperset(answers_ids):
                    self._errors['answers'] = f'not enough answers, (expected {questions_ids}, got {answers_ids})'
                    return False
                if not questions_ids.intersection(answers_ids):
                    self._errors['answers'] = f'extra answers, (expected {questions_ids}, got {answers_ids})'
                    return False
                self._errors['answers'] = f'not enough answers and/or extra answers (expected {questions_ids}, got {answers_ids})'
                return False
            for i, a in enumerate(self.validated_data['answers']):
                if a['answer'] not in questions[a['question'].pk]:
                    print(questions[a['question'].pk])
                    self._errors['answer'] = f'invalid answer {a["answer"]} for question {a["question"].pk}'
                    return False
        return base

    def create(self, validated_data):
        print(validated_data)
        answers = validated_data['answers']
        poll = self._poll
        poll_result, = PollResult.objects.create(poll=poll, user=self.context['request'].user.student.training_suggestor_user),
        for answer in answers:
            PollAnswer.objects.create(result=poll_result, **answer)
        return poll_result

    class Meta:
        model = PollResult
        fields = ('poll', 'answers')
