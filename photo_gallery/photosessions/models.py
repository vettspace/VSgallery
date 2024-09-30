"""Модели для фотосессий и фотографий"""

import os
import shutil
import uuid
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image


def photo_upload_path(instance, filename):
    """Путь для загрузки фотографий."""
    return f'photosessions/{instance.session.id}/{filename}'


class PhotoSession(models.Model):
    """Модель для фотосессии."""
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=100)
    unique_link = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """Удаление папок с фотографиями и превью"""
        photos_dir = os.path.join(
            settings.MEDIA_ROOT, 'photos', str(self.id))
        thumbnails_dir = os.path.join(
            settings.MEDIA_ROOT, 'thumbnails', str(self.id))

        if os.path.exists(photos_dir):
            shutil.rmtree(photos_dir)
        if os.path.exists(thumbnails_dir):
            shutil.rmtree(thumbnails_dir)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


def get_photo_path(instance, filename):
    """Создаем путь вида: photos/<session_id>/<filename>"""
    return os.path.join('photos', str(instance.session.id), filename)


def get_thumbnail_path(instance, filename):
    """Создаем путь вида: thumbnails/<session_id>/<filename>"""
    return os.path.join('thumbnails', str(instance.session.id), filename)


class Photo(models.Model):
    """Модель для фотографий."""
    session = models.ForeignKey(
        PhotoSession, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_photo_path)
    thumbnail = models.ImageField(upload_to=get_thumbnail_path, blank=True)

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            img = Image.open(self.image)
            max_size = (500, 500)
            img.thumbnail(max_size, Image.LANCZOS)
            thumb_io = BytesIO()

            img.save(thumb_io, format='PNG', quality=95)
            thumb_filename = f"thumb_{os.path.splitext(
                os.path.basename(self.image.name))[0]}.png"

            self.thumbnail = InMemoryUploadedFile(
                thumb_io, None, thumb_filename,
                'image/png', thumb_io.tell(), None
            )

        super().save(*args, **kwargs)
