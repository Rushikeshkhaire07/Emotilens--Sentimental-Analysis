import streamlit as st
import spacy
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from transformers import pipeline
import yake

class TextSentimentModule:
    def __init__(self):
        self.emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
        self.nlp = spacy.load("en_core_web_sm")
        self.kw_extractor = yake.KeywordExtractor(
            lan="en",
            n=3,
            dedupLim=0.3,
            top=7,
            features=None
        )
        self.emotion_emojis = {
            "anger": "😠", "disgust": "🤢", "fear": "😨", "joy": "😄",
            "neutral": "😐", "sadness": "😢", "surprise": "😲"
        }
        
    def run(self):
        with st.expander("ℹ️ About this module"):
            st.markdown("""
    <div style="padding:15px; border-radius:10px; background:#f8f9fa;">
    <h3 style="color:#29b6f6; margin-bottom:15px;">Master Your Message ✍️</h3>
    
    ✨ **What text analysis reveals**:
    
    <div style="margin-left:20px; margin-top:10px;">
    
    <br>🔹 <strong>Emotional Layers</strong><br>
   
    - Primary feeling detection<br>
    - Secondary emotion mix<br>
    - Tone consistency
    
    <br>🔹 <strong>Content Effectiveness</strong><br>
    - Readability score<br>
    - Engagement potential<br>
    - Style assessment
    
    <br>🔹 <strong>Writing Enhancements</strong><br>
    - Repetition alerts<br>
    - Complexity analysis<br>
    - Impact suggestions
    
    </div>
    
    <p style="margin-top:15px; color:#666; font-style:italic;">
    Perfect for emails, speeches, surveys, or creative writing!</p>
    </div>
    """, unsafe_allow_html=True)
        
        text_input = st.text_area("Enter your text here:", height=150, help="Type or paste your text for analysis")
        
        if st.button("Analyze Text", use_container_width=True):
            if text_input.strip():
                with st.spinner("🔍 Analyzing your text..."):
                    self.analyze_text(text_input)
            else:
                st.warning("Please enter some text to analyze.")

    def analyze_text(self, text):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Emotion Analysis")
            emotions = self.emotion_classifier(text)[0]
            top_emotion = max(emotions, key=lambda x: x['score'])
            emotions.sort(key=lambda x: x['score'], reverse=True)
            
            st.metric(
                "Main Emotion", 
                f"{top_emotion['label'].capitalize()} {self.emotion_emojis.get(top_emotion['label'], '😐')}", 
                delta=f"{top_emotion['score']*100:.1f}% confidence"
            )
            
            fig, ax = plt.subplots()
            scores = [e['score'] for e in emotions]
            labels = [e['label'].capitalize() for e in emotions]
            ax.barh(labels, scores, color=plt.cm.viridis(np.linspace(0,1,len(labels))))
            ax.set_xlim(0, 1)
            ax.set_title("Emotional Tone Distribution")
            st.pyplot(fig)
        
        with col2:
            st.subheader("📈 Text Overview")
            doc = self.nlp(text)
            
            words = [token.text for token in doc if not token.is_punct]
            num_words = len(words)
            num_sentences = len(list(doc.sents))
            
            cols = st.columns(2)
            cols[0].metric("Total Words", num_words)
            cols[1].metric("Number of Sentences", num_sentences)
            
            st.progress(top_emotion['score'], text=f"Emotion Strength: {top_emotion['score']*100:.1f}%")
            
            wordcloud = WordCloud(
                width=800, 
                height=400,
                background_color='white',
                colormap='viridis',
                max_words=100
            ).generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title("Most Used Words")
            st.pyplot(fig)
        
        # Detailed Analysis section
        st.subheader("🔍 Detailed Analysis")
        tabs = st.tabs([
            "Main Topics", 
            "Word Usage", 
            "Message Clarity",
            "Engagement Level",
            "Communication Style",
            "Key Takeaways"
        ])
        
        with tabs[0]:
            keywords = self.kw_extractor.extract_keywords(text)
            if keywords:
                st.write("### 🎯 Key Topics Discussed")
                for kw, score in keywords:
                    if (1 - score) * 100 > 30:
                        st.write(f"- **{kw}**")
        
        with tabs[1]:
            word_types = Counter([token.pos_ for token in doc])
            friendly_names = {
                'NOUN': 'People, Places, Things',
                'VERB': 'Action Words',
                'ADJ': 'Descriptive Words',
                'ADV': 'Action Modifiers',
                'PRON': 'Pronouns'
            }
            
            plot_data = {friendly_names.get(k, k): v 
                        for k, v in word_types.items() 
                        if k in friendly_names}
            
            if plot_data:
                fig, ax = plt.subplots(figsize=(10, 6))
                wedges, texts, autotexts = ax.pie(
                    plot_data.values(),
                    labels=plot_data.keys(),
                    autopct='%1.1f%%',
                    textprops={'fontsize': 8}
                )
                ax.set_title("Word Distribution")
                plt.setp(autotexts, size=7)
                plt.setp(texts, size=7)
                st.pyplot(fig)

        with tabs[2]:
            st.write("### 📋 Message Clarity Analysis")
            sentences = list(doc.sents)
            avg_len = sum(len([token for token in sent if not token.is_punct]) 
                         for sent in sentences) / len(sentences)
            
            # Clarity insights
            if avg_len < 15:
                clarity_level = "Very Clear"
                clarity_note = "Your message is concise and easy to understand."
            elif avg_len < 25:
                clarity_level = "Clear"
                clarity_note = "Your message maintains good clarity with balanced sentence length."
            else:
                clarity_level = "Complex"
                clarity_note = "Consider breaking down some sentences for better understanding."
            
            st.write(f"**Message Clarity Level:** {clarity_level}")
            st.write(clarity_note)
            
            # Check for repeated words
            word_freq = Counter(token.text.lower() for token in doc if not token.is_stop and not token.is_punct)
            repeated = [word for word, count in word_freq.items() if count > 2]
            if repeated:
                st.write("\n**Frequently Used Words:**")
                st.write("Consider using synonyms for variety:", ", ".join(repeated))

        with tabs[3]:
            st.write("### 🎯 Engagement Analysis")
            
            # Analyze engagement factors
            questions = len([sent for sent in sentences if sent.text.strip().endswith('?')])
            exclamations = len([sent for sent in sentences if sent.text.strip().endswith('!')])
            personal_pronouns = len([token for token in doc if token.pos_ == 'PRON' 
                                  and token.text.lower() in ['i', 'we', 'you']])
            
            engagement_score = min((questions + exclamations) * 20 + personal_pronouns * 10, 100)
            
            st.write("**Engagement Indicators:**")
            if questions > 0:
                st.write(f"- ❓ Contains {questions} questions - creates interaction")
            if exclamations > 0:
                st.write(f"- ❗ Contains {exclamations} emphasis points - adds energy")
            if personal_pronouns > 0:
                st.write("- 👥 Uses personal pronouns - creates connection")
                
            st.progress(engagement_score/100, text=f"Engagement Level: {engagement_score}%")

        with tabs[4]:
            st.write("### 💬 Communication Style")
            
            # Analyze communication style
            formal_indicators = len([token for token in doc if len(token.text) > 6])
            informal_markers = len([token for token in doc if token.text.lower() 
                                 in ['like', 'just', 'maybe', 'pretty', 'kind of']])
            
            style_markers = {
                'Direct': len([sent for sent in sentences if len(sent.text.split()) < 15]),
                'Descriptive': len([token for token in doc if token.pos_ == 'ADJ']),
                'Active': len([token for token in doc if token.pos_ == 'VERB']),
                'Personal': personal_pronouns
            }
            
            dominant_style = max(style_markers.items(), key=lambda x: x[1])[0]
            
            st.write(f"**Primary Communication Style:** {dominant_style}")
            st.write("\n**Style Characteristics:**")
            for style, count in style_markers.items():
                if count > 0:
                    st.write(f"- {style} elements detected")

        with tabs[5]:
            st.write("### 💡 Key Takeaways")
            
            # Generate key insights
            takeaways = []
            
            # Emotion-based takeaway
            if top_emotion['score'] > 0.5:
                takeaways.append(f"Strong {top_emotion['label']} tone suggests {self._get_emotion_insight(top_emotion['label'])}")
            
            # Clarity takeaway
            takeaways.append(f"Message clarity is {clarity_level.lower()} - {self._get_clarity_suggestion(clarity_level)}")
            
            # Engagement takeaway
            if engagement_score > 70:
                takeaways.append("Highly engaging content with good audience connection")
            elif engagement_score > 40:
                takeaways.append("Moderate engagement level - consider adding more interactive elements")
            else:
                takeaways.append("Could benefit from more engaging elements like questions or personal examples")
            
            # Style takeaway
            takeaways.append(f"Communication style is primarily {dominant_style.lower()} - {self._get_style_insight(dominant_style)}")
            
            for takeaway in takeaways:
                st.write(f"- {takeaway}")

    def _get_emotion_insight(self, emotion):
        insights = {
            'joy': "creates a positive and uplifting message",
            'sadness': "may evoke empathy from your audience",
            'anger': "conveys strong conviction or urgency",
            'fear': "highlights important concerns or risks",
            'surprise': "captures attention effectively",
            'neutral': "maintains professional objectivity"
        }
        return insights.get(emotion.lower(), "influences the message tone")

    def _get_clarity_suggestion(self, level):
        suggestions = {
            "Very Clear": "maintains excellent readability",
            "Clear": "effectively balances detail and simplicity",
            "Complex": "could be simplified for broader understanding"
        }
        return suggestions.get(level, "consider audience comprehension")

    def _get_style_insight(self, style):
        insights = {
            'Direct': "gets the message across efficiently",
            'Descriptive': "creates vivid understanding",
            'Active': "keeps the message dynamic",
            'Personal': "builds strong connection with audience"
        }
        return insights.get(style, "suits the content well")