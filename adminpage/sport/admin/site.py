from django.contrib import admin


class SportAdminSite(admin.AdminSite):
    site_header = 'Sport course administration'


site = SportAdminSite()
