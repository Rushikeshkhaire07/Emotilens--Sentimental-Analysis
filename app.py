import streamlit as st
from text_sentiment import TextSentimentModule
from image_sentiment import ImageSentimentModule
from twitter_sentiment import TwitterSentimentModule
from sidebar import setup_sidebar
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SentimentAnalysisApp:
    def __init__(self):
        self.setup_page()
        self.setup_modules()

    def setup_page(self):
        # Configure page once at the start
        st.set_page_config(
            page_title="Sentiment Analysis Hub",
            page_icon="🎭",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Enhanced custom styling with module-specific themes
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                
                body {
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
                }
                
                .stApp {
                    background: transparent;
                }
                
                /* Keyframe Animations */
                @keyframes gradientFlow {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                
                @keyframes subtleGlow {
                    0%, 100% { box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    50% { box-shadow: 0 0 20px rgba(0,0,0,0.2); }
                }
                
                @keyframes floatAndGlow {
                    0%, 100% { 
                        transform: translateY(0);
                        box-shadow: 0 0 15px rgba(0,0,0,0.1);
                    }
                    50% { 
                        transform: translateY(-10px);
                        box-shadow: 0 0 25px rgba(0,0,0,0.2);
                    }
                }
                
                @keyframes colorPulse {
                    0%, 100% { background-color: var(--base-color); }
                    50% { background-color: var(--pulse-color); }
                }
                
                /* Module Container Base */
                .module-container {
                    border-radius: 15px;
                    padding: 2rem;
                    margin: 1rem 0;
                    position: relative;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    animation: subtleGlow 3s infinite alternate;
                }
                
                /* Text Sentiment Module */
                .text-module {
                    --base-color: #f0f9ff;
                    --pulse-color: #e6f2ff;
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    background-size: 200% 200%;
                    color: white;
                    animation: 
                        gradientFlow 10s ease infinite, 
                        floatAndGlow 4s ease-in-out infinite alternate;
                }
                
                .text-module::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(
                        circle, 
                        rgba(52, 152, 219, 0.2) 0%, 
                        transparent 70%
                    );
                    animation: colorPulse 5s infinite alternate;
                }
                
                /* Image Sentiment Module */
                .image-module {
                    background: linear-gradient(135deg, #D1C4E9 0%, #EDE7F6 100%);
                    background-size: 200% 200%;
                    color: white;
                    animation: 
                        gradientFlow 10s ease infinite, 
                        floatAndGlow 5s ease-in-out infinite alternate;
                }
                
                .image-module::after {
                    content: '';
                    position: absolute;
                    bottom: -50%;
                    right: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(
                        circle, 
                        rgba(209, 196, 233, 0.2) 0%, 
                        transparent 70%
                    );
                    animation: colorPulse 6s infinite alternate;
                }
                
                /* Twitter/X Module - Updated to be more bluish and subtle */
                .twitter-module {
                    background: linear-gradient(135deg, #b0d8ff 0%, #81c4ff 100%);
                    background-size: 200% 200%;
                    color: black;
                    animation: 
                        gradientFlow 10s ease infinite, 
                        floatAndGlow 4s ease-in-out infinite alternate;
                }
                
                .twitter-module::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(
                        circle at top right, 
                        rgba(129, 196, 255, 0.2) 0%, 
                        transparent 70%
                    );
                    animation: colorPulse 5s infinite alternate;
                }
                
                /* WhatsApp Module */
                .whatsapp-module {
                    background: linear-gradient(90deg, #d4f1c5 0%, #a8e4a0 100%);
                    background-size: 200% 200%;
                    color: black;
                    animation: 
                        gradientFlow 10s ease infinite, 
                        floatAndGlow 5s ease-in-out infinite alternate;
                }
                
                .whatsapp-module::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    right: 0;
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(
                        circle at bottom right, 
                        rgba(168, 228, 160, 0.2) 0%, 
                        transparent 70%
                    );
                    animation: colorPulse 6s infinite alternate;
                }
                
                /* Module Title Styles */
                .module-title {
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    text-shadow: none;
                    position: relative;
                    z-index: 10;
                }
                
                /* Responsive Adjustments */
                @media (max-width: 768px) {
                    .module-container {
                        padding: 1rem;
                    }
                    .module-title {
                        font-size: 2rem;
                    }
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.title("🔍 Sentiment Analysis Toolkit")

    def setup_modules(self):
        self.module = setup_sidebar()
        self.text_analyzer = TextSentimentModule()
        self.image_analyzer = ImageSentimentModule()
        self.twitter_analyzer = TwitterSentimentModule()

    def run(self):
        with st.container():
            if self.module == "Text Sentiment":
                st.markdown("""
                    <div class='module-container text-module'>
                        <h2 class='module-title'>📝 Text Sentiment Analysis</h2>
                    </div>
                """, unsafe_allow_html=True)
                self.text_analyzer.run()
            
            elif self.module == "Image Sentiment":
                st.markdown("""
                    <div class='module-container image-module'>
                        <h2 class='module-title'>🎭 Image Sentiment Analysis</h2>
                    </div>
                """, unsafe_allow_html=True)
                self.image_analyzer.run()
            
            elif self.module == "X/Twitter Analysis":
                st.markdown("""
                    <div class='module-container twitter-module'>
                        <h2 class='module-title'>🐦 X/Twitter Sentiment Analysis</h2>
                    </div>
                """, unsafe_allow_html=True)
                self.twitter_analyzer.run()

            elif self.module == "WhatsApp Chat Sentiment":
                from whatsapp_sentiment import WhatsAppSentimentModule
                wa_module = WhatsAppSentimentModule()
                st.markdown("""
                    <div class='module-container whatsapp-module'>
                        <h2 class='module-title'>💬 WhatsApp Chat Sentiment Analysis</h2>
                    </div>
                """, unsafe_allow_html=True)
                wa_module.run()

def main():
    app = SentimentAnalysisApp()
    app.run()

if __name__ == "__main__":
    main()
