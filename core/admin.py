from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
    ]
    add_fieldsets = ((None, {"fields": ("username", "email", )}),)

admin.site.register(CustomUser, CustomUserAdmin)
