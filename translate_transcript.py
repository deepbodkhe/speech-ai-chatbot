import json
from googletrans import Translator

def translate_text(text, dest_lang='hi'):  # Default to Hindi
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

def translate_transcript():
    with open("transcript.json", "r") as f:
        transcript = json.load(f)
    
    translated_segments = []
    for segment in transcript['segments']:
        translated_text = translate_text(segment['text'], 'hi')
        translated_segments.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': translated_text
        })
    
    with open("translated.json", "w") as f:
        json.dump({'segments': translated_segments}, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    translate_transcript()
    print("Translation completed and saved to translated.json")