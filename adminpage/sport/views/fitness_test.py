from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def fitness_test_view(request, **kwargs):
    return render(request, "fitness_test.html")
