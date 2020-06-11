from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sport.models import Reference


@login_required
def reference_upload_view(request, **kwargs):
    if request.method == 'POST':
        form = Reference(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, "reference.html")
