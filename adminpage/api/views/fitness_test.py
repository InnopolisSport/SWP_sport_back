def convert_exercises(t) -> dict:
    return {
        "name": t['exercise']['exercise_name'],
        "unit": t['exercise']['value_unit'],
        "score": t['score'],
        "start_range": t['start_range'],
        "end_range": t['end_range']
    }

