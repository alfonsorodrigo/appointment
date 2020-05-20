from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Pediatrician, AppointmentScheduling, Appointment
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",)}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password1",)}),
    )


admin.site.site_header = "Yema Test Alfonso"
admin.site.register(User, UserAdmin)
admin.site.register(Pediatrician)
admin.site.register(AppointmentScheduling)
admin.site.register(Appointment)
