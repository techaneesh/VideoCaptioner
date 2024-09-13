from celery import shared_task
from .models import Video, Subtitle
import subprocess
import os

@shared_task
def extract_subtitles(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path
    output_subtitle_path = video_path.replace('.mp4', '.srt')
    
    # Using ffmpeg to extract subtitles
    command = f'ffmpeg -i {video_path} -map 0:s:0 {output_subtitle_path}'
    subprocess.run(command, shell=True)
    
    # Read and save subtitle content to the database
    with open(output_subtitle_path, 'r') as f:
        subtitle_text = f.read()
    
    Subtitle.objects.create(video=video, language='en', subtitle_text=subtitle_text)
    os.remove(output_subtitle_path)  # Clean up after processing
