from apps.user.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class ActiveUserAdmin(UserAdmin):
    add_form_fields = {
        "classes": ("wide",),
        "fields": ("username", "user_role", "password1", "password2"),
    }
    add_fieldsets = ((None, add_form_fields),)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "user_role")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, ActiveUserAdmin)
