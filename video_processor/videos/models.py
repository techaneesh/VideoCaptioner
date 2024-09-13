from django.db import models

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    subtitle_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
