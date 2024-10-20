from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser, Movie


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    """Register the CustomUser model with the UserAdmin interface for administration purposes."""


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Register the Movie model with the MovieAdmin class to customize its display in the Django admin panel."""

    fields = (
        "title",
        "genre",
        "year",
        "created_date",
        "updated_date",
    )
    list_display = (
        "title",
        "genre",
        "year",
        "created_date",
        "updated_date",
    )
    readonly_fields = (
        "created_date",
        "updated_date",
    )
