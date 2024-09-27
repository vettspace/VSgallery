"""Модели для фотосессий и фотографий"""

import os
import uuid

from django.db import models


def photo_upload_path(instance, filename):
    return f'photosessions/{instance.session.id}/{filename}'


class PhotoSession(models.Model):
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=100)
    unique_link = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    session = models.ForeignKey(
        PhotoSession, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=photo_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo {self.id} in {self.session.title}'
