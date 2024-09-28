"""Галерея для клиентов."""


import os
import zipfile

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import PhotoSession


def gallery_view(request, unique_link):
    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    return render(request, 'photosessions/gallery.html', {'session': session})


def download_photo(request, unique_link, photo_id):
    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    photo = get_object_or_404(session.photos, id=photo_id)
    response = HttpResponse(photo.image, content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(photo.image.name)}"'
    return response


def download_all_photos(request, unique_link):
    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    zip_filename = f"{session.title}_photos.zip"
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zipf:
        for photo in session.photos.all():
            zipf.write(photo.image.path, os.path.basename(photo.image.name))

    return response
