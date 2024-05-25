from django.contrib import admin

from .models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "uuid"]
    filter_horizontal = ["groups", "user_permissions"]
