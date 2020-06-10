from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def reference_upload_view(request, **kwargs):
    return render(request, "reference.html")
