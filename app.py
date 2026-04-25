# app.py - Main Streamlit Application
import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av

# Import modules
from modules import SpeechToText, EmotionDetector, NLPAnalyzer, ScoringSystem, FeedbackGenerator

# Page config
st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    .feedback-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .feedback-success {
        background-color: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }
    .feedback-warning {
        background-color: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    .feedback-info {
        background-color: #d1ecf1;
        border-left-color: #17a2b8;
        color: #0c5460;
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'current_score' not in st.session_state:
    st.session_state.current_score = None
if 'current_feedback' not in st.session_state:
    st.session_state.current_feedback = None
if 'audio_text' not in st.session_state:
    st.session_state.audio_text = ""

# Video processor for emotion detection
class EmotionProcessor(VideoProcessorBase):
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.frame_count = 0
    
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1
        
        # Update emotion every 15 frames
        if self.frame_count % 15 == 0:
            emotion, confidence = self.emotion_detector.update_emotion(img)
        
        # Get current emotion
        emotion, confidence = self.emotion_detector.get_current_emotion()
        
        # Draw emotion on frame
        emotion_colors = {
            'happy': (0, 255, 0),
            'neutral': (255, 255, 0),
            'sad': (255, 0, 0),
            'fear': (255, 165, 0),
            'angry': (0, 0, 255),
            'surprise': (255, 192, 203)
        }
        color = emotion_colors.get(emotion, (255, 255, 255))
        
        # Overlay
        cv2.rectangle(img, (10, 10), (280, 80), (0, 0, 0), -1)
        cv2.putText(img, f"Emotion: {emotion.upper()}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(img, f"Confidence: {confidence:.0%}", (20, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
    def get_emotion(self):
        return self.emotion_detector.get_current_emotion()
    
    def get_dominant_emotion(self):
        return self.emotion_detector.get_dominant_emotion()

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Interview Analyzer</h1>
        <p>Real-time emotion detection + Speech analysis + Instant feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Settings")
        
        questions = {
            "Tell me about yourself": "Tell me about your background and experience.",
            "What are your strengths?": "What are your greatest strengths?",
            "Why should we hire you?": "Why are you the best candidate for this role?",
            "Describe a challenge": "Describe a difficult challenge you overcame.",
            "Teamwork experience": "Tell me about a successful team project.",
            "Career goals": "Where do you see yourself in 5 years?"
        }
        
        selected_question = st.selectbox("Select Question", list(questions.keys()))
        current_question = questions[selected_question]
        
        st.markdown("---")
        st.info("""
        **💡 Tips:**
        - Look at the camera
        - Speak clearly
        - Answer for 30-60 seconds
        - Use specific examples
        """)
    
    # Main layout
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("🎥 Live Camera Feed")
        
        # WebRTC streamer
        ctx = webrtc_streamer(
            key="interview-camera",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=EmotionProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        # Display current emotion
        if ctx and ctx.video_processor:
            emotion, confidence = ctx.video_processor.get_emotion()
            emoji = {'happy':'😊','neutral':'😐','sad':'😔','fear':'😨','angry':'😠','surprise':'😲'}.get(emotion, '😐')
            st.markdown(f"""
            <div class="metric-box">
                <h3>{emoji} Current Emotion: {emotion.upper()}</h3>
                <p>Confidence: {confidence:.0%}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🎤 Record Your Answer")
        
        # Audio recording
        audio_file = st.audio_input("Record your answer", key="audio_recorder")
        
        if audio_file:
            with st.spinner("🎙️ Transcribing your answer..."):
                # Save audio to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    f.write(audio_file.getvalue())
                    audio_path = f.name
                
                # Transcribe
                stt = SpeechToText()
                text = stt.transcribe(audio_path)
                
                if text:
                    st.session_state.audio_text = text
                    st.success("✅ Transcription complete!")
                    st.write("**Your Answer:**")
                    st.info(text)
                    
                    # Cleanup
                    os.unlink(audio_path)
                else:
                    st.error("❌ Could not understand audio. Please try again.")
        
        # Analyze button
        if st.session_state.audio_text and st.button("📊 Analyze My Answer", type="primary", use_container_width=True):
            with st.spinner("Analyzing your interview..."):
                # Get emotion
                if ctx and ctx.video_processor:
                    emotion = ctx.video_processor.get_dominant_emotion()
                    _, emotion_conf = ctx.video_processor.get_emotion()
                else:
                    emotion = "neutral"
                    emotion_conf = 0.5
                
                # NLP Analysis
                nlp = NLPAnalyzer()
                nlp_result = nlp.analyze(st.session_state.audio_text)
                
                # Scoring
                scorer = ScoringSystem()
                score_result = scorer.calculate_score(nlp_result, emotion, emotion_conf)
                
                # Feedback
                fb_generator = FeedbackGenerator()
                feedback = fb_generator.generate_feedback(nlp_result, score_result)
                summary = fb_generator.generate_summary(score_result)
                
                # Store results
                st.session_state.current_score = score_result
                st.session_state.current_feedback = feedback
                st.session_state.current_summary = summary
                st.session_state.current_nlp = nlp_result
                
                st.session_state.answers.append({
                    'question': current_question,
                    'score': score_result['final_score'],
                    'emotion': emotion,
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'words': nlp_result['word_count']
                })
                
                st.rerun()
    
    with col2:
        st.subheader("📊 Dashboard")
        
        if st.session_state.current_score:
            score = st.session_state.current_score
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score['final_score'],
                title={"text": "FINAL SCORE", "font": {"size": 20}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": score['color']},
                    "steps": [
                        {"range": [0, 50], "color": "#ffcccc"},
                        {"range": [50, 70], "color": "#ffffcc"},
                        {"range": [70, 85], "color": "#ccffcc"},
                        {"range": [85, 100], "color": "#00cc00"}
                    ]
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            # Score card
            st.markdown(f"""
            <div class="score-card">
                <h1 style="font-size: 48px;">{score['final_score']:.0f}%</h1>
                <h2>{score['grade']}</h2>
                <p>{score['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown
            st.subheader("Score Breakdown")
            breakdown_df = pd.DataFrame({
                'Category': ['Content', 'Emotion'],
                'Score': [score['breakdown']['content'], score['breakdown']['emotion']]
            })
            fig2 = px.bar(breakdown_df, x='Category', y='Score', text='Score', color='Category')
            fig2.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
            fig2.update_layout(showlegend=False, height=250, yaxis_range=[0, 100])
            st.plotly_chart(fig2, use_container_width=True)
            
            # NLP Details
            if 'current_nlp' in st.session_state:
                nlp = st.session_state.current_nlp
                with st.expander("📝 Content Details"):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.metric("Keywords", f"{nlp['keyword_score']:.0f}%")
                    with col_b:
                        st.metric("Length", f"{nlp['word_count']} words")
                    with col_c:
                        st.metric("Grammar", f"{nlp['grammar_score']:.0f}%")
                    with col_d:
                        st.metric("Clarity", f"{nlp['clarity_score']:.0f}%")
            
            # Feedback
            if st.session_state.current_feedback:
                st.subheader("💡 Feedback & Tips")
                for fb in st.session_state.current_feedback:
                    css_class = f"feedback-{fb['type']}"
                    st.markdown(f"""
                    <div class="feedback-card {css_class}">
                        <strong>{fb['title']}</strong><br>
                        {fb['message']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Summary
            if 'current_summary' in st.session_state:
                st.info(st.session_state.current_summary)
        
        else:
            st.info("""
            ### 👆 Ready to Practice?
            
            1. **Select a question** from sidebar
            2. **Look at the camera** (emotion detection)
            3. **Record your answer** using microphone
            4. **Click "Analyze"** for instant feedback
            
            Your emotions will be detected in real-time!
            """)
    
    # History section
    if st.session_state.answers:
        st.markdown("---")
        st.subheader("📜 Practice History")
        
        hist_df = pd.DataFrame(st.session_state.answers)
        st.dataframe(hist_df[['question', 'score', 'emotion', 'words', 'time']], use_container_width=True)
        
        # Progress chart
        if len(st.session_state.answers) > 1:
            fig3 = px.line(hist_df, x='time', y='score', markers=True, title="Score Progress")
            fig3.update_traces(line=dict(color='#4CAF50', width=3))
            st.plotly_chart(fig3, use_container_width=True)
        
        # Average score
        avg_score = sum(a['score'] for a in st.session_state.answers) / len(st.session_state.answers)
        best_score = max(a['score'] for a in st.session_state.answers)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col_m2:
            st.metric("Best Score", f"{best_score:.1f}%")
        with col_m3:
            st.metric("Total Attempts", len(st.session_state.answers))

if __name__ == "__main__":
    main()