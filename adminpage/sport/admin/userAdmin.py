from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput
from django.db import models
from django.utils.safestring import mark_safe
from hijack.contrib.admin import HijackUserAdminMixin

from .site import site

User = get_user_model()


@admin.register(User, site=site)
class UserAdmin(HijackUserAdminMixin, DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    class Media:
        js = ('admin/js/copyable_email.js',)

    def copyable_email(self, obj):
        email = obj.email
        html = f"""{email}</a><span class="copy-email" onclick="copyToClipboard('{email}')"><svg height="12px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M17.5 14H19C20.1046 14 21 13.1046 21 12V5C21 3.89543 20.1046 3 19 3H12C10.8954 3 10 3.89543 10 5V6.5M5 10H12C13.1046 10 14 10.8954 14 12V19C14 20.1046 13.1046 21 12 21H5C3.89543 21 3 20.1046 3 19V12C3 10.8954 3.89543 10 5 10Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg></span><a>"""
        return mark_safe(html)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "role",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("copyable_email", "first_name", "last_name", "role", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
