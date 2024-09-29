"""Страница просмотра галерей."""


import os
import zipfile

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PhotoForm, PhotoSessionForm
from .models import Photo, PhotoSession


def gallery_view(request, unique_link):
    """Галерея для клиентов."""
    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    is_creator = session.client_name == request.user.username
    return render(
        request,
        'photosessions/gallery.html',
        {'session': session, 'is_creator': is_creator})


def download_photo(request, unique_link, photo_id):
    """Скачать фотографию."""
    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    photo = get_object_or_404(session.photos, id=photo_id)
    response = HttpResponse(photo.image, content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{
        os.path.basename(photo.image.name)}"'
    return response


def download_all_photos(request, unique_link):
    """Скачать все фотографии в zip-архив."""

    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    zip_filename = f"{session.title}_photos.zip"
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zipf:
        for photo in session.photos.all():
            zipf.write(photo.image.path, os.path.basename(photo.image.name))

    return response


@login_required
def create_gallery(request):
    if request.method == 'POST':
        session_form = PhotoSessionForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if session_form.is_valid() and photo_form.is_valid():
            photo_session = session_form.save(commit=False)
            photo_session.client_name = request.user.username
            photo_session.save()

            for file in request.FILES.getlist('images'):
                Photo.objects.create(session=photo_session, image=file)

            return redirect('gallery_list')
    else:
        session_form = PhotoSessionForm()
        photo_form = PhotoForm()

    return render(request, 'photosessions/create_gallery.html', {
        'session_form': session_form,
        'photo_form': photo_form
    })


@login_required
def gallery_list(request):
    """Список галерей пользователя с пагинацией."""
    sessions = PhotoSession.objects.filter(client_name=request.user.username)
    paginator = Paginator(sessions, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'photosessions/gallery_list.html', {'page_obj': page_obj})


@login_required
def delete_gallery(request, unique_link):
    """Удаление галереи."""
    session = get_object_or_404(PhotoSession, unique_link=unique_link)
    if request.user.username == session.client_name:
        session.delete()
    return redirect('gallery_list')
