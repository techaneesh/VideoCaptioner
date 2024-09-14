import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from .models import Video, Subtitle
import os

# def upload_video(request):
#     if request.method == 'POST':
#         video = request.FILES['video']
#         video_obj = Video.objects.create(video_file=video)
#         # Process video subtitles synchronously
#         extract_subtitles(video_obj.id)  # This is now synchronous
#         return JsonResponse({'message': 'Video uploaded and subtitles have been processed.'})
#     return render(request, 'upload.html')
def upload_video(request):
    if request.method == 'POST':
        video = request.FILES['video']
        video_obj = Video.objects.create(video_file=video)

        # Extract subtitles synchronously
        extract_subtitles(video_obj.id)

        # Fetch subtitles
        subtitles = Subtitle.objects.filter(video=video_obj)
        subtitle_data = [
            {
                'language': subtitle.language,
                'subtitle_text': subtitle.subtitle_text
            }
            for subtitle in subtitles
        ]
        
        return JsonResponse({
            'message': 'Video uploaded and is being processed.',
            'subtitles': subtitle_data
        })
    return render(request, 'upload.html')

def extract_subtitles(video_id):
    video = Video.objects.get(id=video_id)
    print(video_id)
    video_path = video.video_file.path
    output_subtitle_path = video_path.replace('.mkv', '.vtt')
    # output_subtitle_path = video_path.rsplit('.', 1)[0] + '.srt'
    
    # Using ffmpeg to extract subtitles
    command = f'ffmpeg -i {video_path} -map 0:s:0 {output_subtitle_path} -f vtt'
    subprocess.run(command, shell=True)
    
    # Read and save subtitle content to the database
    with open(output_subtitle_path, 'r') as f:
        subtitle_text = f.read()
    
    Subtitle.objects.create(video=video, language='en', subtitle_text=subtitle_text)
    # os.remove(output_subtitle_path)  # Clean up after processing


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
