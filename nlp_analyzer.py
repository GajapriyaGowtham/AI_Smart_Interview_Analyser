# modules/nlp_analyzer.py
import re
from textblob import TextBlob

class NLPAnalyzer:
    """Analyze interview answers for content quality"""
    
    def __init__(self):
        self.keywords = [
            'experience', 'skills', 'project', 'team', 'learned', 'achieved',
            'passionate', 'developed', 'solved', 'improved', 'lead', 'successful',
            'built', 'created', 'managed', 'delivered', 'results', 'accomplished',
            'collaborated', 'initiated', 'implemented', 'designed', 'launched'
        ]
        
        self.filler_words = [
            'um', 'uh', 'like', 'actually', 'basically', 'literally',
            'you know', 'sort of', 'kind of', 'well', 'so'
        ]
    
    def analyze(self, text):
        """
        Analyze answer text and return scores
        
        Args:
            text: Interview answer text
            
        Returns:
            Dictionary with analysis results
        """
        text_lower = text.lower()
        words = len(text.split())
        sentences = max(1, text.count('.') + text.count('!') + text.count('?'))
        
        # Keyword score (40%)
        keyword_matches = sum(1 for kw in self.keywords if kw in text_lower)
        keyword_score = min(1.0, keyword_matches / len(self.keywords))
        
        # Length score (25%)
        if 50 <= words <= 150:
            length_score = 1.0
        elif 30 <= words <= 200:
            length_score = 0.7
        else:
            length_score = 0.4
        
        # Grammar/Sentence structure (20%)
        avg_words_per_sentence = words / sentences
        if 10 <= avg_words_per_sentence <= 20:
            grammar_score = 1.0
        elif 5 <= avg_words_per_sentence <= 30:
            grammar_score = 0.7
        else:
            grammar_score = 0.4
        
        # Clarity (15%)
        filler_count = sum(1 for f in self.filler_words if f in text_lower)
        clarity_score = max(0, 1 - (filler_count / max(words, 1)) * 10)
        
        # Sentiment analysis
        blob = TextBlob(text)
        sentiment_score = (blob.sentiment.polarity + 1) / 2
        
        # Overall score
        overall = (
            keyword_score * 0.40 +
            length_score * 0.25 +
            grammar_score * 0.20 +
            clarity_score * 0.15
        ) * 100
        
        return {
            'overall_score': overall,
            'keyword_score': keyword_score * 100,
            'length_score': length_score * 100,
            'grammar_score': grammar_score * 100,
            'clarity_score': clarity_score * 100,
            'sentiment_score': sentiment_score * 100,
            'word_count': words,
            'sentence_count': sentences,
            'filler_word_count': filler_count
        }
    
    def extract_keywords(self, text):
        """Extract important keywords from answer"""
        text_lower = text.lower()
        found = [kw for kw in self.keywords if kw in text_lower]
        return found[:5]