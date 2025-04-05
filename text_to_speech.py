from gtts import gTTS
import json

def text_to_speech():
    with open("translated.json", "r") as f:
        data = json.load(f)
    
    full_text = " ".join([seg['text'] for seg in data['segments']])
    tts = gTTS(full_text, lang='hi')
    tts.save("output_audio.mp3")

if __name__ == "__main__":
    text_to_speech()
    print("Audio generated as output_audio.mp3")