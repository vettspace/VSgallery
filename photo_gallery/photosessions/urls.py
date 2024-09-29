from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateGalleryView.as_view(), name='create_gallery'),
    path('list/', views.GalleryListView.as_view(), name='gallery_list'),
    path('delete/<uuid:unique_link>/',
         views.DeleteGalleryView.as_view(), name='delete_gallery'),
    path('<uuid:unique_link>/', views.GalleryView.as_view(), name='gallery'),
    path('download/<uuid:unique_link>/photo/<int:photo_id>/',
         views.DownloadPhotoView.as_view(), name='download_photo'),
    path('download/<uuid:unique_link>/all/',
         views.DownloadAllPhotosView.as_view(), name='download_all_photos'),
]
