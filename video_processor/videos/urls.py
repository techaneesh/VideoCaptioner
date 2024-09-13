from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('subtitles/<int:video_id>/', views.video_subtitles, name='video_subtitles'),
    path('search/', views.search_subtitles, name='search_subtitles'),
]
