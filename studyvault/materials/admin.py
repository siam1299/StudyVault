# materials/admin.py
from django.contrib import admin
from .models import Category, Department, SemesterYear, Material
from .models import University


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(SemesterYear)
class SemesterYearAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "uploader", "category", "department", "semester", "download_count", "created_at")
    list_filter = ("category", "department", "semester", "created_at")
    search_fields = ("title", "description", "uploader__username")
    autocomplete_fields = ("uploader", "category", "department", "semester")
    readonly_fields = ("download_count", "created_at", "updated_at")
    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "description", "uploader")
        }),
        ("Classification", {
            "fields": ("category", "department", "semester")
        }),
        ("File", {
            "fields": ("file", )
        }),
        ("Stats", {
            "fields": ("download_count", "created_at", "updated_at")
        }),
    )

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
