import re
from yt_dlp import YoutubeDL
import os

def download_nrk_to_wav(video_url: str, output_folder="./downloads"):
    """
    Downloads an audio file from an NRK video and converts it to WAV format.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            "ffmpeg_location": 'C:/ProgramData/chocolatey/bin/ffmpeg.exe',
            "ffprobe_location" 'C:/ProgramData/chocolatey/bin/ffprobe.exe'
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            extract_video_name = info.get('title', 'Unknown Video')
            video_name = re.sub(r'[<>:"/\\|?*.,()\[\]\-]', '', extract_video_name)
            language_info = info.get('language')

        ydl_opts['outtmpl'] = os.path.join(output_folder, f"{video_name}.%(ext)s")

        with YoutubeDL(ydl_opts) as ydl:
            if not os.path.exists(os.path.join(output_folder, f"{video_name}.wav")):
                ydl.download([video_url])

        language = language_info if language_info else 'no'  # Default to Norwegian

        os.environ["LANGUAGE"] = language
        properties_to_update = {
            "LANGUAGE": language,
            "FILE_NAME": f"{video_name}",
            "FRONTEND_VIDEO_URL": f"{video_url}",
            "STREAM_NAME": f"{video_name}",
            "VIDEO_NAME": f"{video_name}",
            "FILE": f"downloads/{video_name}.wav"
        }
        jsonl_file = f"/data/transcripts_{language}_{video_name}.jsonl"
        return jsonl_file, properties_to_update
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
