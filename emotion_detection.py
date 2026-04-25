import cv2
import numpy as np
from collections import Counter
import threading
import math

class EmotionDetector:
    """Improved emotion detection using facial landmarks and features"""
    
    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_confidence = 0.5
        self.emotion_history = []
        self.lock = threading.Lock()
        
        # Load face cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Load eye cascade for better detection
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
        # Load smile cascade
        self.smile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml'
        )
    
    def detect_faces(self, frame):
        """Detect faces in frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            # Return the largest face
            return max(faces, key=lambda rect: rect[2] * rect[3])
        return None
    
    def detect_smile(self, face_roi):
        """Detect smile in face region"""
        try:
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            smiles = self.smile_cascade.detectMultiScale(
                gray_face, 
                scaleFactor=1.7, 
                minNeighbors=22,
                minSize=(25, 25)
            )
            return len(smiles) > 0, len(smiles)
        except:
            return False, 0
    
    def detect_eyes(self, face_roi):
        """Detect eyes in face region"""
        try:
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            eyes = self.eye_cascade.detectMultiScale(
                gray_face, 
                scaleFactor=1.1, 
                minNeighbors=10,
                minSize=(20, 20)
            )
            return len(eyes)
        except:
            return 0
    
    def calculate_mouth_aspect_ratio(self, face_roi):
        """Calculate mouth aspect ratio to detect smile/expression"""
        try:
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            # Focus on lower half of face (mouth region)
            mouth_region = gray[int(height*0.6):, :]
            
            # Calculate brightness and contrast of mouth region
            mouth_brightness = np.mean(mouth_region)
            mouth_std = np.std(mouth_region)
            
            # Smile detection through brightness and contrast
            if mouth_brightness > 120 and mouth_std > 30:
                return 1.0  # Likely smiling
            elif mouth_brightness > 100:
                return 0.6  # Slight smile
            else:
                return 0.2  # Not smiling
        except:
            return 0.3
    
    def analyze_eyebrow_position(self, face_roi):
        """Analyze eyebrow position for emotion detection"""
        try:
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            # Upper half of face (eyebrow region)
            eyebrow_region = gray[0:int(height*0.3), :]
            eyebrow_brightness = np.mean(eyebrow_region)
            eyebrow_std = np.std(eyebrow_region)
            
            # Detect furrowed brows (angry/fear)
            if eyebrow_std < 20 and eyebrow_brightness < 80:
                return "furrowed"
            # Neutral brows
            elif 80 <= eyebrow_brightness <= 120:
                return "neutral"
            # Raised brows (surprise)
            else:
                return "raised"
        except:
            return "neutral"
    
    def analyze_emotion(self, face_roi):
        """Comprehensive emotion analysis using multiple features"""
        
        # Get features
        has_smile, smile_count = self.detect_smile(face_roi)
        eye_count = self.detect_eyes(face_roi)
        mouth_ratio = self.calculate_mouth_aspect_ratio(face_roi)
        brow_position = self.analyze_eyebrow_position(face_roi)
        
        # Emotion scoring
        emotions = {
            'happy': 0,
            'sad': 0,
            'angry': 0,
            'surprise': 0,
            'neutral': 0
        }
        
        # Smile detection
        if has_smile or mouth_ratio > 0.7:
            emotions['happy'] += 0.8
            emotions['neutral'] += 0.2
        elif mouth_ratio > 0.5:
            emotions['happy'] += 0.5
            emotions['neutral'] += 0.4
        
        # Eye detection (fewer eyes might indicate squinting/anger)
        if eye_count < 2:
            emotions['angry'] += 0.3
            emotions['sad'] += 0.2
        
        # Eyebrow position
        if brow_position == "furrowed":
            emotions['angry'] += 0.6
            emotions['fear'] += 0.3
        elif brow_position == "raised":
            emotions['surprise'] += 0.6
            emotions['happy'] += 0.2
        
        # Mouth ratio for sadness (downturned mouth simulation)
        if mouth_ratio < 0.3:
            emotions['sad'] += 0.5
        
        # Get the emotion with highest score
        if max(emotions.values()) > 0:
            dominant_emotion = max(emotions, key=emotions.get)
            confidence = emotions[dominant_emotion]
            
            # Adjust confidence
            if dominant_emotion == 'happy' and has_smile:
                confidence = min(0.95, confidence + 0.2)
            
            return dominant_emotion, confidence
        else:
            return "neutral", 0.5
    
    def update_emotion(self, frame):
        """Update current emotion from frame"""
        try:
            # Detect face
            face = self.detect_faces(frame)
            
            if face is not None:
                x, y, w, h = face
                # Extract face region with some margin
                margin = int(w * 0.1)
                x1 = max(0, x - margin)
                y1 = max(0, y - margin)
                x2 = min(frame.shape[1], x + w + margin)
                y2 = min(frame.shape[0], y + h + margin)
                face_roi = frame[y1:y2, x1:x2]
                
                # Analyze emotion
                if face_roi.size > 0:
                    emotion, confidence = self.analyze_emotion(face_roi)
                    
                    with self.lock:
                        self.current_emotion = emotion
                        self.emotion_confidence = confidence
                        self.emotion_history.append(emotion)
                        
                        # Keep only last 100 history items
                        if len(self.emotion_history) > 100:
                            self.emotion_history = self.emotion_history[-100:]
                    
                    return emotion, confidence
            
            # No face detected
            return "neutral", 0.3
                
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return "neutral", 0.5
    
    def get_current_emotion(self):
        """Get current detected emotion"""
        with self.lock:
            return self.current_emotion, self.emotion_confidence
    
    def get_dominant_emotion(self):
        """Get most frequent emotion from session"""
        with self.lock:
            if self.emotion_history:
                return Counter(self.emotion_history).most_common(1)[0][0]
            return "neutral"
    
    def get_emotion_score(self, emotion=None):
        """Convert emotion to confidence score (0-1)"""
        if emotion is None:
            emotion = self.get_dominant_emotion()
        
        emotion_scores = {
            'happy': 1.0,
            'surprise': 0.85,
            'neutral': 0.6,
            'sad': 0.35,
            'fear': 0.3,
            'angry': 0.2,
            'disgust': 0.1
        }
        return emotion_scores.get(emotion, 0.5)