# twitter_sentiment.py (Updated)
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import re
import requests
from datetime import datetime, timedelta
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from transformers import pipeline
import os


class TwitterSentimentModule:
    def __init__(self):
        self.TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
        self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                           model="cardiffnlp/twitter-roberta-base-sentiment")
        self.stop_words = set(stopwords.words('english'))
        self._download_nltk_resources()

    def _download_nltk_resources(self):
        try:
            stopwords.words('english')
        except LookupError:
            import nltk
            nltk.download('stopwords')

    def _clean_tweet(self, text):
        """Clean and preprocess tweet text"""
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        # Remove special characters except basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()

    def _analyze_sentiment(self, text):
        """Analyze sentiment of individual tweets"""
        try:
            result = self.sentiment_analyzer(text[:512])[0]  # Truncate to model max length
            return result['label'].lower()
        except Exception as e:
            st.error(f"Error analyzing sentiment: {str(e)}")
            return "neutral"

    def run(self):
        # Twitter Module Expander
        with st.expander("ℹ️ About this module", expanded=False):
             st.markdown("""
    <div style="padding:15px; border-radius:10px; background:#f8f9fa;">
    <h3 style="color:#1DA1F2; margin-bottom:15px;">Decode Social Media Buzz 📈</h3>
    
    ✨ **What you'll discover about public conversations**:
    
    <div style="margin-left:20px; margin-top:10px;">
                         
    <br>🔹 <strong>Real-Time Trends</strong><br>
    
    - Current topic discussions<br>
    - Popular hashtags & keywords<br>
    - Viral content patterns
    
    <br>🔹 <strong>Crowd Emotion Map</strong><br>
    - Positive/negative ratio<br>
    - Hourly sentiment changes<br>
    - Controversy detection
    
    <br>🔹 <strong>Audience Insights</strong><br>
    - Peak engagement times<br>
    - Most active user periods<br>
    - Discussion longevity
    
    </div>
    
    <p style="margin-top:15px; color:#666; font-style:italic;">
    Ideal for brand monitoring, event tracking, or social research!</p>
    </div>
    """, unsafe_allow_html=True)

        if not self.TWITTER_BEARER_TOKEN:
            st.error("Twitter API credentials not found in environment variables")
            return
            
        topic = st.text_input("Enter search topic:", "AI")
        num_tweets = st.slider("Number of tweets to analyze:", 10, 50)
        
        if st.button("Analyze Tweets"):
            with st.spinner("Fetching and analyzing tweets..."):
                tweets = self._fetch_tweets(topic, num_tweets)
                if tweets:
                    self._process_and_display(tweets)
                else:
                    st.error("No tweets found or API error")

    def _fetch_tweets(self, topic, num_tweets):
        headers = {"Authorization": f"Bearer {self.TWITTER_BEARER_TOKEN}"}
        params = {
            "query": f"{topic} -is:retweet",
            "max_results": num_tweets,
            "tweet.fields": "created_at,public_metrics",
            "start_time": (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
        }
        
        try:
            response = requests.get(
                "https://api.twitter.com/2/tweets/search/recent",
                headers=headers,
                params=params
            )
            if response.status_code == 200:
                return response.json().get('data', [])
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def _process_and_display(self, tweets):
        df = pd.DataFrame(tweets)
        df['text'] = df['text'].apply(self._clean_tweet)
        df['sentiment'] = df['text'].apply(self._analyze_sentiment)
        
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🔍 Details"])
        
        with tab1:
            self._display_wordcloud(df)
            self._sentiment_distribution(df)
            
        with tab2:
            self._temporal_analysis(df)
            
        with tab3:
            self._display_tweets_table(df)

    def _display_wordcloud(self, tweets):
        text = " ".join(tweets['text'])
        wordcloud = WordCloud(width=800, height=400, background_color='white',
                             stopwords=self.stop_words).generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    def _sentiment_distribution(self, tweets):
        sentiment_counts = tweets['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['sentiment', 'count']
        fig = px.pie(sentiment_counts, names='sentiment', values='count', 
                    title="Sentiment Distribution", hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    def _temporal_analysis(self, tweets):
        tweets['created_at'] = pd.to_datetime(tweets['created_at'])
        tweets['hour'] = tweets['created_at'].dt.hour
        fig = px.histogram(tweets, x='hour', color='sentiment', 
                         title="Activity by Hour", barmode='stack',
                         color_discrete_map={
                             'positive': '#2CA02C',
                             'neutral': '#1F77B4',
                             'negative': '#D62728'
                         })
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

    def _display_tweets_table(self, tweets):
        st.dataframe(
            tweets[['created_at', 'text', 'sentiment']],
            column_config={
                "created_at": "Timestamp",
                "text": "Tweet",
                "sentiment": st.column_config.SelectboxColumn(
                    "Sentiment",
                    options=["positive", "neutral", "negative"]
                )
            },
            hide_index=True,
            use_container_width=True
        )