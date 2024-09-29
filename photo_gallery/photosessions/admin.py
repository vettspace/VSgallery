"""Админка для фотографий."""

from django.contrib import admin

from .models import Photo, PhotoSession


class PhotoInline(admin.TabularInline):
    """Класс для отображения фотографий в админке."""
    model = Photo
    extra = 1


class PhotoSessionAdmin(admin.ModelAdmin):
    """Админка для фотосессии."""
    list_display = ['title', 'client_name', 'unique_link', 'created_at']
    inlines = [PhotoInline]


admin.site.register(PhotoSession, PhotoSessionAdmin)
