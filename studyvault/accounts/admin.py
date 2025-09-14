from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "university", "department")
    search_fields = ("user__username", "university__name", "department__name")
