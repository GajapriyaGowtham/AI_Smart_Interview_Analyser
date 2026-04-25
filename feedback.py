# modules/feedback.py

class FeedbackGenerator:
    """Generate personalized feedback based on analysis"""
    
    def generate_feedback(self, nlp_result, score_result):
        """
        Generate detailed feedback
        
        Args:
            nlp_result: Results from NLPAnalyzer
            score_result: Results from ScoringSystem
            
        Returns:
            List of feedback messages
        """
        feedback = []
        
        # Content feedback
        if nlp_result['keyword_score'] < 40:
            feedback.append({
                'type': 'warning',
                'title': 'Add More Keywords',
                'message': 'Use more industry-specific keywords and technical terms from the job description.'
            })
        elif nlp_result['keyword_score'] < 70:
            feedback.append({
                'type': 'info',
                'title': 'Good Keyword Usage',
                'message': 'You\'re using relevant keywords. Try adding more specific examples.'
            })
        else:
            feedback.append({
                'type': 'success',
                'title': 'Excellent Keyword Usage',
                'message': 'Great use of relevant keywords and industry terms!'
            })
        
        # Length feedback
        if nlp_result['word_count'] < 40:
            feedback.append({
                'type': 'warning',
                'title': 'Answer Too Short',
                'message': f'Your answer is {nlp_result["word_count"]} words. Aim for 50-150 words for optimal responses.'
            })
        elif nlp_result['word_count'] > 150:
            feedback.append({
                'type': 'warning',
                'title': 'Answer Too Long',
                'message': f'Your answer is {nlp_result["word_count"]} words. Try to be more concise (50-150 words ideal).'
            })
        else:
            feedback.append({
                'type': 'success',
                'title': 'Good Answer Length',
                'message': f'Your answer length ({nlp_result["word_count"]} words) is ideal!'
            })
        
        # Filler words feedback
        if nlp_result['filler_word_count'] > 3:
            feedback.append({
                'type': 'warning',
                'title': 'Reduce Filler Words',
                'message': f'Found {nlp_result["filler_word_count"]} filler words. Try to reduce "um", "like", "actually".'
            })
        
        # Sentence structure
        if nlp_result['sentence_count'] < 3:
            feedback.append({
                'type': 'info',
                'title': 'Use More Sentences',
                'message': 'Break your answer into multiple sentences for better flow and structure.'
            })
        
        # Emotion feedback
        emotion = score_result['details']['detected_emotion']
        if emotion == 'happy':
            feedback.append({
                'type': 'success',
                'title': 'Great Confidence!',
                'message': 'Your positive emotions show confidence. Keep it up!'
            })
        elif emotion == 'neutral':
            feedback.append({
                'type': 'info',
                'title': 'Show More Enthusiasm',
                'message': 'Try to show more positive emotions and energy in your responses.'
            })
        elif emotion in ['sad', 'fear', 'angry']:
            feedback.append({
                'type': 'warning',
                'title': 'Work on Confidence',
                'message': 'Practice relaxation techniques and confident body language before interviews.'
            })
        
        return feedback
    
    def generate_summary(self, score_result):
        """Generate a quick summary"""
        final_score = score_result['final_score']
        
        if final_score >= 85:
            summary = "🎉 Excellent interview! You're well-prepared and confident."
        elif final_score >= 70:
            summary = "👍 Good interview! A few improvements will make you stand out."
        elif final_score >= 50:
            summary = "📚 Good start! Focus on the improvement tips for next time."
        else:
            summary = "💪 Keep practicing! Review the feedback and try again."
        
        return summary