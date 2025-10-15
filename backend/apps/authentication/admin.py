from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "profile", "is_active", "is_staff")
    list_filter = ("profile", "is_active", "is_staff")
    search_fields = ("username", "email")
