import os
import subprocess
import whisper
import torch
import tempfile
import time

def download_youtube_livestream_to_wav(video_url: str, output_folder="./downloads"):
    """
    Streams YouTube livestream audio using yt-dlp and ffmpeg,
    processes it in real-time, and transcribes speech to text in smaller snippets.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Temporary WAV file to store small audio chunks
    temp_wav_file = os.path.join(tempfile.gettempdir(), "livestream_audio.wav")

    # yt-dlp command to extract only live content (without history)
    yt_dlp_command = [
        "yt-dlp",
        "-f", "bestaudio",
        "-o", "-",  
        video_url
    ]

    # FFmpeg command to split live audio into ultra-short segments for faster transcription
    ffmpeg_command = [
        "ffmpeg",
        "-i", "pipe:0",
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-f", "segment",
        "-segment_time", "2",  # Process audio every 2 seconds
        "-y",
        temp_wav_file
    ]

    # Run yt-dlp & FFmpeg in a subprocess pipeline
    yt_dlp_process = subprocess.Popen(yt_dlp_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=yt_dlp_process.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("Livestream audio is being captured... Transcribing in real-time.")

    # Check if a GPU is available and load Whisper accordingly
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}") 

    # Load Whisper model 
    model = whisper.load_model("base").to("cuda")

    try:
        last_transcription = ""  # Keep track of last snippet to avoid duplicates

        while True:
            # Check if the small WAV file has been written
            if os.path.exists(temp_wav_file):
                print(temp_wav_file)
                time.sleep(0.5)  # Wait briefly for FFmpeg to write chunk
                
                # Transcribe only the most recent segment
                result = model.transcribe(
                    temp_wav_file, 
                    fp16=True if device == "cuda" else False,
                    word_timestamps=True  
                )
                
                transcript = result["text"].strip()

                # Print and store the transcript if it's new
                if transcript and transcript != last_transcription:
                    print(f"Live Transcript: {transcript}")  # Immediate output
                    last_transcription = transcript  # Avoid duplicate prints

                    # Append the transcript to a file
                    with open(os.path.join(output_folder, "livestream_transcript.txt"), "a", encoding="utf-8") as f:
                        f.write(transcript + "\n")

    except KeyboardInterrupt:
        print("Stopping livestream recording...")
        yt_dlp_process.terminate()
        ffmpeg_process.terminate()

    return os.path.join(output_folder, "livestream_transcript.txt")

# Example Usage:
#download_youtube_livestream_to_wav("https://www.youtube.com/watch?v=YDfiTGGPYCk")
download_youtube_livestream_to_wav("https://tv.nrk.no/direkte/nrk1")
