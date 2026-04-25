# modules/speech_to_text.py
import speech_recognition as sr
import tempfile
import os

class SpeechToText:
    """Convert speech to text using Google Speech Recognition"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe(self, audio_file_path):
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to audio file (WAV/MP3)
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def transcribe_bytes(self, audio_bytes):
        """Transcribe audio from bytes"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_bytes)
                f.flush()
                text = self.transcribe(f.name)
            os.unlink(f.name)
            return text
        except Exception as e:
            print(f"Error: {e}")
            return None