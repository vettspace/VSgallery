import os
import zipfile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import FormView

from .forms import PhotoForm, PhotoSessionForm
from .models import Photo, PhotoSession


class GalleryView(DetailView):
    """Отображение фотографий внутри фотосессии."""
    model = PhotoSession
    template_name = 'photosessions/gallery.html'
    context_object_name = 'session'
    slug_field = 'unique_link'
    slug_url_kwarg = 'unique_link'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_creator'] = self.object.client_name == self.request.user.username
        return context


class DownloadPhotoView(DetailView):
    """Скачивание фотографии."""
    model = Photo

    def get(self, request, *args, **kwargs):
        photo = self.get_object()
        response = HttpResponse(photo.image, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{
            os.path.basename(photo.image.name)}"'
        return response

    def get_object(self):
        """Получение объекта фотографии."""
        session = get_object_or_404(
            PhotoSession, unique_link=self.kwargs['unique_link'])
        return get_object_or_404(session.photos, id=self.kwargs['photo_id'])


class DownloadAllPhotosView(DetailView):
    """Скачивание всех фотографий внутри фотосессии."""
    model = PhotoSession
    slug_field = 'unique_link'
    slug_url_kwarg = 'unique_link'

    def get(self, request, *args, **kwargs):
        session = self.get_object()
        zip_filename = f"{session.title}_photos.zip"
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={
            zip_filename}'

        with zipfile.ZipFile(response, 'w') as zipf:
            for photo in session.photos.all():
                zipf.write(photo.image.path,
                           os.path.basename(photo.image.name))

        return response


class CreateGalleryView(LoginRequiredMixin, FormView):
    """Создание новой галереи."""
    template_name = 'photosessions/create_gallery.html'
    form_class = PhotoSessionForm
    success_url = reverse_lazy('gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = PhotoForm()
        return context

    def form_valid(self, form):
        photo_form = PhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            photo_session = form.save(commit=False)
            photo_session.client_name = self.request.user.username
            photo_session.save()

            for file in self.request.FILES.getlist('images'):
                Photo.objects.create(session=photo_session, image=file)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class GalleryListView(LoginRequiredMixin, ListView):
    """Список галерей пользователя."""
    model = PhotoSession
    template_name = 'photosessions/gallery_list.html'
    context_object_name = 'sessions'
    paginate_by = 10

    def get_queryset(self):
        return PhotoSession.objects.filter(client_name=self.request.user.username)


class DeleteGalleryView(LoginRequiredMixin, DeleteView):
    """Удаление галереи."""
    model = PhotoSession
    success_url = reverse_lazy('gallery_list')
    slug_field = 'unique_link'
    slug_url_kwarg = 'unique_link'

    def get_queryset(self):
        return PhotoSession.objects.filter(client_name=self.request.user.username)
