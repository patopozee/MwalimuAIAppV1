# voice.py
import os
import io
import base64
import requests

# Grab your OpenRouter key from the environment
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def speech_to_text(audio_bytes):
    """
    Sends audio bytes to OpenRouter's Speech-to-Text API by encoding it to Base64.
    """
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY environment variable is missing."
    if not audio_bytes:
        return ""

    try:
        # OpenRouter STT expects a raw base64 string (no data URI prefix)
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        url = "https://openrouter.ai/api/v1/audio/transcriptions"
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Request payload specifically tailored for OpenRouter's STT format
        payload = {
            "model": "openai/whisper-1",
            "input_audio": {
                "data": base64_audio,
                "format": "wav"  # mic_recorder outputs WAV data by default
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result_json = response.json()
        return result_json.get("text", "").strip()
        
    except Exception as e:
        return f"OpenRouter Whisper transcription failed: {str(e)}"

def text_to_speech(text, student_profile=None):
    """
    Placeholder system fallback helper. 
    """
    pass