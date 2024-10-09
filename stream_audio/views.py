from django.http import StreamingHttpResponse
import subprocess

def stream_audio(request):
    video_id = request.GET.get('id')  # Get the YouTube video URL from query parameters
    video_url = "https://www.youtube.com/watch?v=" + video_id
    if not video_url:
        return StreamingHttpResponse("No URL provided.", status=400)

    # Command to stream audio using yt-dlp
    command = [
        'yt-dlp',
        '-f', 'bestaudio',  # Select best audio format
        '-o', '-',          # Output to stdout
        video_url
    ]

    # Start the yt-dlp process
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    # Stream the audio using ffmpeg
    ffmpeg_command = [
        'ffmpeg',
        '-i', 'pipe:0',      # Input from stdin
        '-f', 'mp3',         # Output format
        'pipe:1'             # Output to stdout
    ]

    # Start ffmpeg process
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=process.stdout, stdout=subprocess.PIPE)

    def generate_audio_chunks():
        try:
            while True:
                chunk = ffmpeg_process.stdout.read(1024)  # Read in chunks of 1024 bytes
                if not chunk:
                    break
                yield chunk  # Yield each chunk to the response

        finally:
            process.kill()
            ffmpeg_process.kill()

    return StreamingHttpResponse(generate_audio_chunks(), content_type='audio/mpeg')