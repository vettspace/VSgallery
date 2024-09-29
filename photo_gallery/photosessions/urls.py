from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_gallery, name='create_gallery'),
    path('list/', views.gallery_list, name='gallery_list'),
    path('delete/<uuid:unique_link>/', views.delete_gallery, name='delete_gallery'),
    path('<uuid:unique_link>/', views.gallery_view, name='gallery'),
    path('download/<uuid:unique_link>/photo/<int:photo_id>/', views.download_photo, name='download_photo'),
    path('download/<uuid:unique_link>/all/', views.download_all_photos, name='download_all_photos'),
]
