import json
import os
import yt_dlp
from transformers import pipeline

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio',  # Output file name
        'quiet': True,       # Suppress console output
        'extract_audio': True,  # Extract audio without FFmpeg
        'preferredcodec': 'mp3',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return 'audio.mp3'  # yt-dlp automatically adds extension
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise

def transcribe_audio(audio_path):
    try:
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small",
            device="cpu"
        )
        result = pipe(audio_path)
        return {"segments": [{"text": result["text"], "start": 0, "end": 300}]}
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        raise

def save_to_json(transcript):
    with open("transcript.json", "w", encoding='utf-8') as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=80UVjkcxGmA"
    audio_path = None  # Initialize variable
    
    try:
        print("Step 1/3: Downloading audio...")
        audio_path = download_audio(video_url)
        
        print("Step 2/3: Transcribing audio...")
        transcript = transcribe_audio(audio_path)
        
        print("Step 3/3: Saving transcript...")
        save_to_json(transcript)
        
        print("✅ Success! Transcript saved to transcript.json")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)