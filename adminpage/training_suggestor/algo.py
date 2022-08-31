from typing import List, Tuple

from django.db.models import QuerySet

from training_suggestor.models import ExerciseParams


def suggest_algo(db: QuerySet[ExerciseParams], working_load: float, time: float, number_of_exercises: int):
    wl_coef, t_coef = 0.01, 0.01  # Задаётся вручную, коэффициенты масштабирования
    db_dict = [{'id': e.id, 'working_load': e.working_load, 'full_time': e.full_time} for e in db]
    print([(e['working_load'], e['full_time'].total_seconds()) for e in db_dict])

    # Алгоритм масштабирования
    # --------
    f = [(int(e['working_load'] * wl_coef), int(e['full_time'].total_seconds() * t_coef), e['id']) for e in db_dict]
    wl = int(working_load * wl_coef)
    t = int(time * t_coef)
    # --------

    dp = [[[False] * (t + 1) for _ in range(wl + 1)] for _ in range(number_of_exercises + 1)]
    parent = [[[(0, 0, -1)] * (t + 1) for _ in range(wl + 1)] for _ in range(number_of_exercises + 1)]
    dp[0][0][0] = True

    for item in f:
        for i in range(wl, -1, -1):
            for j in range(t, -1, -1):
                for k in range(number_of_exercises - 1, -1, -1):
                    if i + item[0] <= wl and j + item[1] <= t and dp[k][i][j] and not dp[k + 1][i + item[0]][j + item[1]]:
                        dp[k + 1][i + item[0]][j + item[1]] = True
                        parent[k + 1][i + item[0]][j + item[1]] = item

    ans_i, ans_j, ans_k = 0, 0, 0
    for k in range(number_of_exercises + 1):
        for i in range(wl + 1):
            for j in range(t + 1):
                if dp[k][i][j] and (i + j + k) > (ans_i + ans_j + ans_k):
                    ans_i, ans_j, ans_k = i, j, k

    # print(ans_i / wl_coef, ans_j / t_coef)

    exercises: List[ExerciseParams] = []

    while ans_i > 0 or ans_j > 0:
        temp = parent[ans_k][ans_i][ans_j]
        ans_i -= temp[0]
        ans_j -= temp[1]
        ans_k -= 1
        # print(temp[2])
        exercises.append(db.get(id=temp[2]))
    return exercises
