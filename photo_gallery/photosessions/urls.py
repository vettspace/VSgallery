from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:unique_link>/', views.gallery_view, name='gallery'),
    path('download/<uuid:unique_link>/photo/<int:photo_id>/',
         views.download_photo, name='download_photo'),
    path('download/<uuid:unique_link>/all/',
         views.download_all_photos, name='download_all_photos'),
]
