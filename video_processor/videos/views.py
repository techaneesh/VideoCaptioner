from django.shortcuts import render
from django.http import JsonResponse
from .models import Video, Subtitle
from .tasks import extract_subtitles
import os

def upload_video(request):
    if request.method == 'POST':
        video = request.FILES['video']
        video_obj = Video.objects.create(video_file=video)
        # Call background task to process video
        extract_subtitles.delay(video_obj.id)
        return JsonResponse({'message': 'Video uploaded and is being processed.'})
    return render(request, 'upload.html')

def search_subtitles(request):
    query = request.GET.get('q')
    if query:
        results = Subtitle.objects.filter(subtitle_text__icontains=query)
        response_data = [{'video': res.video.id, 'timestamp': res.subtitle_text.find(query)} for res in results]
        return JsonResponse({'results': response_data})
    return JsonResponse({'error': 'No query provided'})

def video_subtitles(request, video_id):
    subtitles = Subtitle.objects.filter(video_id=video_id)
    subtitle_data = [{'language': sub.language, 'text': sub.subtitle_text} for sub in subtitles]
    return JsonResponse({'subtitles': subtitle_data})

