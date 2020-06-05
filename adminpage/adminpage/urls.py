"""adminpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

# TODO: remove when not needed
# from django.http import JsonResponse
# def show(request):
#     data = dict(
#         [
#             (key, str(value)) for key, value in request.META.items()
#         ]
#     )
#     data.update({
#         "scheme": str(request.scheme),
#     })
#     return JsonResponse(data)


urlpatterns = [
                  path(settings.PREFIX, include([
                      # path('admin/test', show),
                      path('admin/', admin.site.urls),
                      path('oauth2/', include('django_auth_adfs.urls')),
                      path('login/', LoginView.as_view(
                          redirect_authenticated_user=True,
                      )),
                      url(r"api/", include("api.urls")),
                  ]))
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT,
                         )
