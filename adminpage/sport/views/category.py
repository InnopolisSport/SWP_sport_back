from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.crud import get_sports, get_clubs, get_sc_training_group


@login_required
def category_view(request, **kwargs):
    sports = get_sports()
    clubs = sorted(
        [{
            "available_places": club["capacity"] - club["current_load"],
            **club,
        }
            for club in get_clubs()],
        key=lambda group: (group["current_load"] >= group["capacity"], group["name"])
    )
    sc_training_group_id = get_sc_training_group()["id"]
    return render(request, "category.html", {
        "sports": sports,
        "clubs": clubs,
        "sc_training_group_id": sc_training_group_id,
    })
