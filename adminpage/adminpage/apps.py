from django.contrib.admin.apps import AdminConfig


class SportAdminConfig(AdminConfig):
    default_site = 'sport.admin.site.SportAdminSite'
