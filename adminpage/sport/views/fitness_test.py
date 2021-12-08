from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def fitness_test_view(request, **kwargs):
    return render(request, "fitness_test.html")


@login_required
def fitness_test_session_view(request, **kwargs):
    # TODO: add fitness_test_session_id
    return render(request, "fitness_test_session.html")
