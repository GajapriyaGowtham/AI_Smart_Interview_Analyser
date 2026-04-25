# modules/scoring.py

class ScoringSystem:
    """Calculate final interview score"""
    
    def __init__(self, weights=None):
        self.weights = weights or {
            'content': 0.70,    # 70% content
            'emotion': 0.30     # 30% emotion
        }
    
    def calculate_score(self, nlp_result, emotion, emotion_confidence):
        """
        Calculate final score based on content and emotion
        
        Args:
            nlp_result: Results from NLPAnalyzer
            emotion: Detected emotion string
            emotion_confidence: Confidence of emotion detection
            
        Returns:
            Dictionary with final score and breakdown
        """
        # Emotion score mapping
        emotion_scores = {
            'happy': 1.0,
            'surprise': 0.85,
            'neutral': 0.6,
            'sad': 0.35,
            'fear': 0.3,
            'angry': 0.2,
            'disgust': 0.1
        }
        
        # Calculate emotion score
        base_emotion_score = emotion_scores.get(emotion, 0.5)
        emotion_score = base_emotion_score * emotion_confidence * 100
        
        # Get content score
        content_score = nlp_result['overall_score']
        
        # Weighted final score
        final_score = (
            content_score * self.weights['content'] +
            emotion_score * self.weights['emotion']
        )
        
        # Determine grade
        if final_score >= 85:
            grade = "Excellent"
            color = "#00cc00"
            recommendation = "Strong Hire"
        elif final_score >= 70:
            grade = "Good"
            color = "#4CAF50"
            recommendation = "Proceed to Next Round"
        elif final_score >= 50:
            grade = "Average"
            color = "#FF9800"
            recommendation = "Consider with Training"
        else:
            grade = "Needs Improvement"
            color = "#f44336"
            recommendation = "Keep Practicing"
        
        return {
            'final_score': final_score,
            'grade': grade,
            'color': color,
            'recommendation': recommendation,
            'breakdown': {
                'content': content_score,
                'emotion': emotion_score
            },
            'details': {
                'content_score': content_score,
                'emotion_score': emotion_score,
                'detected_emotion': emotion,
                'emotion_confidence': emotion_confidence
            }
        }