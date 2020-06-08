from django.shortcuts import render


def handler404(request, exception, template_name="errors/404.html"):
    return render(request, template_name)


def handler505(request, template_name="errors/500.html"):
    return render(request, template_name)
