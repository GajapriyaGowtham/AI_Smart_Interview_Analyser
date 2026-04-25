# 🤖 AI Smart Interview Analyser

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📌 Overview

The **AI Smart Interview Analyser** is an intelligent tool that automates the interview analysis process. It leverages **Speech-to-Text**, **NLP**, and **Emotion Detection** to provide unbiased, data-driven feedback on a candidate's performance, helping recruiters make better hiring decisions.

## 🚀 Key Features

- 🎙️ **Speech-to-Text**: Converts interview audio/video responses to text.
- 🧠 **NLP Analysis**: Analyzes transcribed text for keywords, sentiment, and coherence.
- 😊 **Emotion Detection**: Detects candidate emotions (confidence, hesitation, happiness) from audio.
- 📊 **Automated Scoring**: Generates a performance score based on content & delivery.
- 📝 **Feedback Generation**: Produces actionable, constructive feedback.
- 🌐 **Web Interface**: User-friendly dashboard to upload and analyse interviews.

## 🏗️ Project Structure

AI_Smart_Interview_Analyser/
│
├── app.py # Main FastAPI application
├── speech_to_text.py # Audio transcription module
├── nlp_analyzer.py # Text analysis & NLP logic
├── emotion_detection.py # Emotion recognition from audio
├── scoring.py # Scoring and evaluation logic
├── feedback.py # Feedback generation module
├── requirements.txt # Python dependencies
├── init.py # Package initializer
└── README.md # Project documentation


## 🔧 Technical Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Python |
| **Speech-to-Text** | Google Speech / Whisper / Vosk |
| **NLP** | Hugging Face Transformers, spaCy |
| **Emotion Detection** | Audio analysis (Librosa, PyAudio) |
| **Frontend** | HTML/CSS/JavaScript (inside `app.py`) |
| **Deployment** | Uvicorn, Ngrok (for Colab) |

## 🚀 Quick Start

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/GajapriyaGowtham/AI_Smart_Interview_Analyser.git
cd AI_Smart_Interview_Analyser

# Install dependencies
pip install -r requirements.txt

Run the Application
# Start the FastAPI server
python app.py

# The application will be available at:
# http://localhost:8000

📊 Usage Flow

Upload Audio/Video
       ↓
Speech-to-Text Transcription
       ↓
NLP Analysis (Content + Sentiment)
       ↓
Emotion Detection (Audio features)
       ↓
Scoring & Feedback Generation
       ↓
Display Results to Recruiter

🎯 Sample Output
The analyser provides:

{
  "transcription": "I have 5 years of experience in Python...",
  "sentiment_score": 0.85,
  "keywords_found": ["Python", "leadership", "teamwork"],
  "emotion_analysis": {
    "confidence": 0.92,
    "hesitation": 0.12,
    "enthusiasm": 0.78
  },
  "overall_score": 87.5,
  "feedback": "Strong technical skills. Improve confidence in vocal delivery."
}

📁 Modules Explanation
Module	Purpose
speech_to_text.py	Handles audio conversion to text
nlp_analyzer.py	Analyzes content relevance, sentiment, and grammar
emotion_detection.py	Detects emotions from audio tone and pitch
scoring.py	Combines all metrics to calculate final score
feedback.py	Generates readable, actionable feedback
🔄 Future Enhancements
Add video facial expression analysis (CV)

Support for multiple languages

Dashboard for comparing multiple candidates

API integration with Zoom/Google Meet

Real-time analysis during live interviews

🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📧 Contact
Author: Gajapriya Gowtham
GitHub: @GajapriyaGowtham

🙏 Acknowledgments
OpenAI Whisper / Google Speech-to-Text

Hugging Face Transformers

FastAPI community
