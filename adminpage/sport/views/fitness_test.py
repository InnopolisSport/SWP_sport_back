from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def fitness_test_view(request, **kwargs):
    return render(request, "fitness_test.html")


@login_required
def fitness_test_session_view(request, fitness_test_session_id, **kwargs):
    return render(request, "fitness_test_session.html")


@login_required
def fitness_test_session_new_view(request, **kwargs):
    return render(request, "fitness_test_session.html")
