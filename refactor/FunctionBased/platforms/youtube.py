import re
from yt_dlp import YoutubeDL
import os


def download_youtube_to_wav(video_url: str, output_folder="./downloads"):
    """Downloads a YouTube video as WAV using yt-dlp and ffmpeg."""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # Ensure FFmpeg paths are correctly set
        ffmpeg_path = "C:/ProgramData/chocolatey/bin/ffmpeg.exe"
        ffprobe_path = "C:/ProgramData/chocolatey/bin/ffprobe.exe"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
            "ffmpeg_location": ffmpeg_path, 
            "ffprobe_location": ffprobe_path, 
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "postprocessor_args": [
                "-ar", "16000",  # Optional: Set sample rate (16kHz, common for speech)
                "-ac", "1"       # Optional: Convert to mono audio
            ],
            "keepvideo": False,  # Ensure only audio remains
            "noplaylist": True,  # Avoid downloading entire playlists
        }

        # Extract video metadata before downloading
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            extract_debate_name = info.get("title", "Unknown Debate")
            debate_name = re.sub(r'[<>:"/\\|?*.,()\[\]\-]', "", extract_debate_name)
            language_info = info.get("language")

        # Set output file path for proper conversion
        ydl_opts["outtmpl"] = os.path.join(output_folder, f"{debate_name}.%(ext)s")

        # Ensure correct WAV file generation
        wav_file_path = os.path.join(output_folder, f"{debate_name}.wav")
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)  # Remove existing WAV to avoid overwriting issues

        # Download the audio
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Assign language metadata (default to English if none found)
        language = language_info if language_info else "en"
        os.environ["LANGUAGE"] = language

        properties_to_update = {
            "LANGUAGE": language,
            "FILE_NAME": debate_name,
            "FRONTEND_VIDEO_URL": video_url,
            "STREAM_NAME": debate_name,
            "DEBATE_NAME": debate_name,
            "FILE": f"downloads/{debate_name}.wav",
        }
        jsonl_file = f"/data/transcripts_{language}_{debate_name}.jsonl"

        # Ensure WAV file exists after processing
        if not os.path.exists(wav_file_path):
            raise FileNotFoundError(f"Failed to convert to WAV: {wav_file_path}")

        return jsonl_file, properties_to_update

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
