"""Админка для фотографий."""

from django.contrib import admin

from .models import Photo, PhotoSession


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


class PhotoSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'unique_link', 'created_at']
    inlines = [PhotoInline]


admin.site.register(PhotoSession, PhotoSessionAdmin)
