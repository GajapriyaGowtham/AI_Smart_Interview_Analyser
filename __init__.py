# modules/__init__.py
from .speech_to_text import SpeechToText
from .emotion_detection import EmotionDetector
from .nlp_analyzer import NLPAnalyzer
from .scoring import ScoringSystem
from .feedback import FeedbackGenerator

__all__ = [
    'SpeechToText',
    'EmotionDetector', 
    'NLPAnalyzer',
    'ScoringSystem',
    'FeedbackGenerator'
]