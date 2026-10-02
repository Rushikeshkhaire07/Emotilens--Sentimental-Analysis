# home.py
import streamlit as st
import random

def floating_animation():
    st.markdown("""
    <style>
    /* Updated Hero Inner Container */
    .hero-inner {
        position: relative;
        z-index: 10;
        text-align: center;
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Updated Tagline Styling */
    .tagline {
        font-size: 1.75rem;
        color: rgba(220,220,220,0.85);
        font-style: italic;
        font-weight: bold;
        margin: 1.5rem auto;
        position: relative;
        display: block;
        width: 100%;
        text-align: center;
        line-height: 1.4;
        white-space: nowrap;
    }

    .tagline::after {
        content: '';
        display: block;
        height: 3px;
        margin: 8px auto 0 auto;
        background: linear-gradient(90deg, #ff6b6b, #f7d794, #6ab04c, #686de0, #f0932b);
        background-size: 200% auto;
        border-radius: 2px;
        animation: shimmer 4s linear infinite;
        width: 100%;
    }

    /* Media Query for Mobile Responsiveness */
    @media (max-width: 768px) {
        .hero-inner {
            padding: 1rem;
        }
        
        .title-text {
            font-size: 4rem;
        }
        
        .tagline {
            font-size: 1.25rem;
            white-space: normal;
        }
    }

    /* Floating & Gradient Animations */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Title Pulse Animation */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Shimmer animation for underline */
    @keyframes shimmer {
        0% { background-position: 200% center; }
        100% { background-position: -200% center; }
    }
    
    /* Hero Container Styling with a Colorful Gradient Background */
    .hero-container {
        position: relative;
        overflow: hidden;
        padding: 8rem 2rem 4rem;
        background: linear-gradient(135deg, #ff6b6b, #f7d794, #6ab04c, #686de0, #f0932b);
        background-size: 200% 200%;
        animation: gradientFlow 15s ease infinite;
        border-radius: 2rem;
        margin: -2rem;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    }
    
    /* Title Styling */
    .title-text {
        font-family: 'Poppins', sans-serif;
        font-size: 6rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff6b6b, #f7d794, #6ab04c, #686de0, #f0932b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        animation: pulse 3s ease-in-out infinite;
    }
    
    /* Feature Card Styling with Equal Height */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 1.5rem;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 300px;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.15);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        background: linear-gradient(45deg, #ff6b6b, #f7d794, #6ab04c, #686de0, #f0932b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: float 4s ease-in-out infinite;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #f7d794, #6ab04c, #686de0, #f0932b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 4rem 0 2rem;
        text-align: center;
        position: relative;
    }
    
    /* Particle Effects */
    .particle {
        position: absolute;
        pointer-events: none;
        animation: float 6s infinite ease-in-out;
        opacity: 0.9;
    }
    
    .glow {
        position: absolute;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        filter: blur(80px);
        z-index: -1;
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # Generate 30 particles in a scattered fashion (with some overlap)
    particles = ["😊", "😢", "😨", "😡", "😮", "😐", "😭", "😂", "🤫"]
    for i in range(30):
        emoji = random.choice(particles)
        left_pos = random.uniform(2, 98)
        top_pos = random.uniform(0, 8)
        font_size = random.uniform(1.5, 3)
        delay = random.uniform(0, 3)
        st.markdown(f"""
        <div class="particle" style="
            left: {left_pos}%;
            top: {top_pos}%;
            font-size: {font_size}rem;
            animation-delay: {delay}s;
        ">{emoji}</div>
        """, unsafe_allow_html=True)

def show_home():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: #0f172a;
        color: white;
    }
    
    .stApp {
        background: linear-gradient(225deg, #0f172a 0%, #1e293b 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    floating_animation()
    
    st.markdown("""
    <div class="hero-container">
        <div class="hero-inner">
            <div class="title-text">EmotiLens</div>
            <div class="tagline">See Beyond the Surface with Data-Driven Insights</div>
        </div>
        <div class="glow" style="top: 10%; left: 25%;"></div>
        <div class="glow" style="bottom: 10%; right: 25%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Why EmotiLens?</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌌</div>
            <h3 style="color: white; margin: 0 0 1rem 0;">Multidimensional Analysis</h3>
            <p style="color: rgba(255,255,255,0.8);">
              Uncover hidden patterns across text, images, and social interactions
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 style="color: white; margin: 0 0 1rem 0;">Data-Driven Insights</h3>
            <p style="color: rgba(255,255,255,0.8);">
              Combining cutting-edge analytics for precision analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3 style="color: white; margin: 0 0 1rem 0;">Visual Mastery</h3>
            <p style="color: rgba(255,255,255,0.8);">
             Interactive visualizations and dynamic dashboards
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Getting Started</div>', unsafe_allow_html=True)
    
    steps = [
        {"icon": "🚀", "title": "Choose Module", "text": "Select your analysis type from the sleek sidebar"},
        {"icon": "📤", "title": "Upload Content", "text": "Drag & drop your files or paste text directly"},
        {"icon": "🔮", "title": "Discover Insights", "text": "Explore interactive visualizations and actionable insights"}
    ]
    
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="text-align: center;">
                <div class="feature-icon" style="font-size: 2.5rem;">{steps[i]['icon']}</div>
                <h4 style="color: white; margin: 1rem 0;">{steps[i]['title']}</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 0;">{steps[i]['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="divider"></div>
    <style>
    .divider {
      width: 80%;
      height: 3px;
      margin: 4rem auto;
      background: linear-gradient(90deg, #ff6b6b, #f7d794, #6ab04c, #686de0, #f0932b);
      background-size: 200% auto;
      border-radius: 2px;
      animation: shimmer 4s linear infinite;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_home()
