import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from wordcloud import WordCloud
from datetime import datetime
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
import calendar
import os
from io import BytesIO

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Title Container */
    .title-container {
        background: linear-gradient(90deg, #25D366 0%, #128C7E 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Already styled metrics */
    .stMetric {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .stMetric:hover {
        transform: scale(1.05);
    }
    
    /* Section Title Styling */
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 20px;
        color: #333;
        text-align: center;
    }
    
    /* Insight Section Container with Animation */
    .insight-section {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
                
    </style>
    """, unsafe_allow_html=True)

class WhatsAppSentimentModule:
    def __init__(self):
        inject_custom_css()
        self.theme_colors = {
            'positive': '#2ECC71',   # Green
            'negative': '#E74C3C',   # Red
            'neutral': '#F39C12',    # Yellow
            'primary': '#25D366',
            'secondary': '#128C7E'
        }
    
    def run(self):
        # WhatsApp Module Expander
        with st.expander("ℹ️ About this module", expanded=False):
            st.markdown("""
    <div style="padding:15px; border-radius:10px; background:#f8f9fa;">
    <h3 style="color:#128C7E; margin-bottom:15px;">Discover Your Chat's Hidden Story 💬</h3>
    
    ✨ **What this reveals about your conversations**:
    
    <div style="margin-left:20px; margin-top:10px;">
                        
    <br>🔹 <strong>Group Activity</strong><br>
    - Who talks most & when<br>
    - Daily/weekly chat patterns<br>
    - Peak conversation times
    
    <br>🔹 <strong>Content Insights</strong><br>
    - Most shared links & media<br>
    - Popular topics & keywords<br>
    - Frequently used emojis
    
    <br>🔹 <strong>Emotional Pulse</strong><br>
    - Overall mood trends<br>
    - Positive/negative moments<br>
    - Sentiment timeline
    
    </div>
    
    <p style="margin-top:15px; color:#666; font-style:italic;">
    Perfect for understanding family groups, team chats, or friend circles!</p>
    </div>
    """, unsafe_allow_html=True)

        # New Input Method Selection with Hover-help placed AFTER the expander
        input_method = st.radio(
            "Choose input method", 
            ("Upload Chats", "Select Sample Chats"),
            help="Select 'Upload Chats' to upload your own exported WhatsApp chat file or 'Select Sample Chats' to choose from sample chat files to get the Analysis."
        )

        uploaded_file = None
        if input_method == "Upload Chats":
            uploaded_file = st.file_uploader("Upload your exported WhatsApp chat (.txt)", type=['txt'])
        else:
            sample_path = r"C:\Users\HARSHAL\OneDrive\Desktop\New folder (3)\SEN\sample_chats"
            try:
                sample_files = [f for f in os.listdir(sample_path) if f.endswith(".txt")]
            except Exception as e:
                st.error(f"Error accessing sample chats folder: {e}")
                sample_files = []
            if sample_files:
                selected_sample = st.selectbox("Select a sample chat file", sample_files,
                                               help="Select a sample chat file")
                if selected_sample:
                    with open(os.path.join(sample_path, selected_sample), "r", encoding="utf-8") as f:
                        content = f.read()
                    # Convert string to BytesIO to simulate an uploaded file
                    uploaded_file = BytesIO(content.encode("utf-8"))
            else:
                st.warning("No sample chat files found in the sample folder.")
        
        if uploaded_file:
            df = self.parse_chat(uploaded_file)
            if df is not None:
                # Filter by sender
                unique_senders = df['sender'].unique().tolist()
                sender_filter = st.multiselect("Filter by sender:", options=unique_senders, default=unique_senders)
                if sender_filter:
                    df = df[df['sender'].isin(sender_filter)]
                self.display_insights(df)
    
    def parse_chat(self, uploaded_file):
        try:
            # Check if file is in bytes; if not, encode it
            content = uploaded_file.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
        
        pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM))\s*[-–]\s*([^:]+):\s*(.*)'
        data = []
        for line in content.splitlines():
            match = re.match(pattern, line)
            if match:
                try:
                    date_str, time_str, sender, message = match.groups()
                    dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%y %I:%M %p")
                    data.append({
                        "datetime": dt, 
                        "sender": sender, 
                        "message": message,
                        "words": len(message.split()),
                        "media": "media" in message.lower(),
                        "links": len(re.findall(r'http[s]?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message))
                    })
                except ValueError:
                    continue
            else:
                if data:
                    data[-1]["message"] += " " + line.strip()
        
        if not data:
            st.error("No chat messages found. Please check the file format.")
            return None
        
        return pd.DataFrame(data)
    
    def display_insights(self, df):
        # -------------------- Top Statistics --------------------
        st.markdown('<h2 class="section-title">📊 Top Statistics</h2>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.metric("Total Messages", len(df))
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.metric("Total Words", df['words'].sum())
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.metric("Media Shared", df['media'].sum())
            st.markdown("</div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.metric("Links Shared", df['links'].sum())
            st.markdown("</div>", unsafe_allow_html=True)
        
        # -------------------- Activity Patterns --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📅 Activity Patterns</h2>', unsafe_allow_html=True)
        
        # Monthly Activity Timeline
        df['month'] = df['datetime'].dt.to_period('M')
        monthly_activity = df.groupby('month').size()
        fig_months = go.Figure(data=go.Scatter(
            x=monthly_activity.index.astype(str), 
            y=monthly_activity.values, 
            mode='lines+markers',
            marker_color=self.theme_colors['primary']
        ))
        fig_months.update_layout(title='Monthly Activity Timeline', 
                                 xaxis_title='Month', 
                                 yaxis_title='Number of Messages')
        st.plotly_chart(fig_months, use_container_width=True)
        
        # Daily Activity Timeline
        df['date'] = df['datetime'].dt.date
        daily_activity = df.groupby('date').size()
        fig_daily = go.Figure(data=go.Scatter(
            x=daily_activity.index.astype(str), 
            y=daily_activity.values, 
            mode='lines+markers',
            marker_color=self.theme_colors['secondary']
        ))
        fig_daily.update_layout(title='Daily Activity Timeline', 
                                 xaxis_title='Date', 
                                 yaxis_title='Number of Messages')
        st.plotly_chart(fig_daily, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------- Most Busy Day --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">🗓 Most Busy Day</h2>', unsafe_allow_html=True)
        df['day_of_week'] = df['datetime'].dt.day_name()  
        day_activity = df.groupby('day_of_week').size()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_activity = day_activity.reindex(day_order)
        fig_busiest_day = go.Figure(data=[go.Bar(
            x=day_activity.index, 
            y=day_activity.values, 
            marker_color=['#1E90FF', '#2E8B57', '#9932CC', '#FF6347', '#FFD700', '#00CED1', '#FF4500']
        )])
        fig_busiest_day.update_layout(title='Most Busy Day', 
                                      xaxis_title='Day', 
                                      yaxis_title='Number of Messages')
        st.plotly_chart(fig_busiest_day, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------- Most Busy Month --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📆 Most Busy Month</h2>', unsafe_allow_html=True)
        monthly_busy = df.groupby('month').size()
        fig_busiest_month = go.Figure(data=[go.Bar(
            x=monthly_busy.index.astype(str), 
            y=monthly_busy.values, 
            marker_color=['#8E44AD', '#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#16A085', '#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#f1c40f', '#e67e22', '#e74c3c', '#ecf0f1', '#95a5a6', '#d35400', '#c0392b', '#bdc3c7', '#7f8c8d', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#2c3e50', '#f39c12', '#ff5733', '#ff6b81', '#48dbfb', '#1e90ff', '#ff9f43', '#00d2d3', '#6c5ce7', '#fd79a8', '#a29bfe', '#dfe6e9', '#ffbe76']
        )])
        fig_busiest_month.update_layout(title='Most Busy Month', 
                                        xaxis_title='Month', 
                                        yaxis_title='Number of Messages')
        st.plotly_chart(fig_busiest_month, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------- Word Cloud --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">☁️ Word Cloud</h2>', unsafe_allow_html=True)
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        words = ' '.join(df['message']).lower().split()
        filtered_words = [word for word in words if word not in stop_words]
        wordcloud = WordCloud(width=800, height=400, 
                              background_color='white', 
                              colormap='viridis').generate(' '.join(filtered_words))
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------- Most Common Words --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">💬 Most Common Words</h2>', unsafe_allow_html=True)
        word_counts = Counter(filtered_words)
        top_15_words = word_counts.most_common(15)
        words_df = pd.DataFrame(top_15_words, columns=['Word', 'Count'])
        fig_words = go.Figure(data=[go.Bar(
            x=words_df['Count'], 
            y=words_df['Word'], 
            orientation='h',
            marker_color=[f'rgba({np.random.randint(50,200)}, {np.random.randint(50,200)}, {np.random.randint(50,200)}, 0.7)' for _ in range(15)]
        )])
        fig_words.update_layout(title='Top 15 Most Common Words', 
                                xaxis_title='Count', 
                                yaxis_title='Word')
        st.plotly_chart(fig_words, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------- Emoji Analysis --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">😀 Emoji Analysis</h2>', unsafe_allow_html=True)
        all_emojis = ''.join(df['message'])
        emoji_counts = Counter(c for c in all_emojis if c in emoji.EMOJI_DATA)
        emoji_df = pd.DataFrame.from_dict(emoji_counts, orient='index', columns=['count']).reset_index()
        emoji_df.columns = ['emoji', 'count']
        emoji_df = emoji_df.sort_values('count', ascending=False).head(10)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df[['emoji', 'count']])
        with col2:
            fig_emojis = go.Figure(data=[go.Pie(
                labels=emoji_df['emoji'], 
                values=emoji_df['count'],
                textinfo='label+percent'
            )])
            fig_emojis.update_layout(title='Top Emojis Used')
            st.plotly_chart(fig_emojis)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------- Sentiment Analysis --------------------
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📈 Sentiment Analysis</h2>', unsafe_allow_html=True)
        
        def categorize_sentiment(score):
            if score > 0.05:
                return 'Positive'
            elif score < -0.05:
                return 'Negative'
            else:
                return 'Neutral'
        
        df['sentiment'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
        df['sentiment_category'] = df['sentiment'].apply(categorize_sentiment)
        sentiment_colors = {
            'Positive': self.theme_colors['positive'],
            'Negative': self.theme_colors['negative'],
            'Neutral': self.theme_colors['neutral']
        }
        sentiment_counts = df['sentiment_category'].value_counts()
        fig_sentiment = go.Figure(data=[go.Bar(
            x=sentiment_counts.index, 
            y=sentiment_counts.values,
            marker_color=[sentiment_colors[cat] for cat in sentiment_counts.index]
        )])
        fig_sentiment.update_layout(title='Sentiment Distribution')
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
        overall_sentiment = df['sentiment'].mean()
        if overall_sentiment > 0.05:
            sentiment_emoji = '😄'
            sentiment_text = 'Positive'
        elif overall_sentiment < -0.05:
            sentiment_emoji = '😞'
            sentiment_text = 'Negative'
        else:
            sentiment_emoji = '😐'
            sentiment_text = 'Neutral'
        st.markdown(f"<h3 style='text-align:center;'>Overall Sentiment: <span style='color:#333;'>{sentiment_text} {sentiment_emoji}</span></h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    analyzer = WhatsAppSentimentModule()
    analyzer.run()

if __name__ == "__main__":
    main()
