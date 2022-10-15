from training_suggestor.models import PollResult


def recalculate_ratios(result: PollResult):
    """Recalculate the ratios for user according to poll"""
    for e in result.answers.all():
        try:
            answer_with_influence: dict = [a for a in e.question.answers if a['answer'] == e.answer][0]
            time_ratio = 1 + answer_with_influence["time_ratio_influence"]
            working_load_ratio = 1 + answer_with_influence["working_load_ratio_influence"]
            result.user.time_ratio *= time_ratio
            result.user.working_load_ratio *= working_load_ratio
            result.user.save()
        except IndexError:
            pass
