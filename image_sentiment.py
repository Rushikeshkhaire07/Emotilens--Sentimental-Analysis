import os
import cv2
import numpy as np
import streamlit as st
from deepface import DeepFace
import matplotlib.pyplot as plt
from mtcnn import MTCNN
from PIL import Image
import base64
from io import BytesIO
import textwrap

class ImageSentimentModule:
    def __init__(self):
        # Updated emotion colors: angry is red, happy is green, etc.
        self.emotion_colors = {
            'angry': '#FF0000',       # red
            'disgust': '#A569BD',     # purple
            'fear': '#5DADE2',        # blue
            'happy': '#28B463',       # green
            'sad': '#6C5CE7',         # purple-blue
            'surprise': '#F5B041',    # orange
            'neutral': '#95A5A6'      # gray
        }
        self.detector = MTCNN()
        self.inject_ui_styles()

    def inject_ui_styles(self):
        st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            * {{
                font-family: 'Inter', sans-serif !important;
            }}
            .main .block-container {{
                max-width: 1200px;
                padding-top: 2rem;
            }}
            .stFileUploader {{
                border: 2px dashed #E0E0E0 !important;
                border-radius: 15px !important;
                padding: 2rem !important;
                transition: all 0.3s ease !important;
            }}
            .stFileUploader:hover {{
                border-color: #4ECDC4 !important;
                background: rgba(78,205,196,0.05) !important;
            }}
            .summary-card {{
                background: white !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
                transition: transform 0.3s ease !important;
                border-left: 4px solid {self.emotion_colors['happy']};
                margin-bottom: 1rem;
            }}
            .summary-card:hover {{
                transform: translateY(-5px);
            }}
            .chart-container {{
                margin-bottom: 20px;
            }}
            .face-container {{
                display: flex;
                overflow-x: auto;
                padding: 20px 0;
                gap: 15px;
            }}
            .face-card {{
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                min-width: 250px;
                padding: 15px;
                transition: transform 0.2s;
            }}
            .face-card:hover {{
                transform: translateY(-5px);
            }}
            .face-image {{
                border-radius: 5px;
                width: 100%;
                height: 200px;
                object-fit: cover;
            }}
            @keyframes chartSlide {{
                0% {{ opacity: 0; transform: translateY(20px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
            .stPlot {{
                animation: chartSlide 0.6s ease-out !important;
            }}
            .stSpinner > div {{
                border-color: {self.emotion_colors['happy']} !important;
                border-right-color: transparent !important;
            }}
            .stMetric {{
                padding: 1rem !important;
                border-radius: 12px !important;
                background: rgba(255, 255, 255, 0.9) !important;
                backdrop-filter: blur(8px) !important;
            }}
            ::-webkit-scrollbar {{
                width: 6px;
                height: 6px;
            }}
            ::-webkit-scrollbar-track {{
                background: rgba(0,0,0,0.05);
            }}
            ::-webkit-scrollbar-thumb {{
                background: {self.emotion_colors['neutral']};
                border-radius: 4px;
            }}
        </style>
        """, unsafe_allow_html=True)

    def detect_faces(self, img):
        """Enhanced face detection using MTCNN"""
        faces = self.detector.detect_faces(img)
        return [(int(face['box'][0]), int(face['box'][1]),
                 int(face['box'][2]), int(face['box'][3])) for face in faces]

    def analyze_faces(self, img, faces):
        results = []
        for (x, y, w, h) in faces:
            try:
                face_img = img[y:y+h, x:x+w]
                analysis = DeepFace.analyze(
                    img_path=face_img,
                    actions=['emotion', 'age', 'gender', 'race'],
                    detector_backend='skip',
                    enforce_detection=False,
                    silent=True
                )
                if isinstance(analysis, list):
                    analysis = analysis[0]
                analysis['region'] = {'x': x, 'y': y, 'w': w, 'h': h}
                analysis['dominant_gender'] = max(analysis['gender'], key=analysis['gender'].get)
                analysis['dominant_race'] = max(analysis['race'], key=analysis['race'].get)
                results.append(analysis)
            except Exception as e:
                continue
        return results

    def draw_faces(self, img, results):
        """Draw bounding boxes and labels on faces"""
        img_draw = img.copy()
        for idx, face in enumerate(results):
            x, y, w, h = face['region'].values()
            emotion = max(face['emotion'], key=face['emotion'].get)
            color = tuple(int(self.emotion_colors[emotion].lstrip('#')[i:i+2], 16)
                          for i in (0, 2, 4))
            cv2.rectangle(img_draw, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img_draw, f"Person {idx+1}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        return img_draw

    def create_emotion_chart(self, results):
        """Create a bar chart of emotion distribution with larger dimensions"""
        emotions_data = {}
        for face in results:
            for emotion, score in face['emotion'].items():
                emotions_data[emotion] = emotions_data.get(emotion, 0) + score / len(results)
        plt.figure(figsize=(14, 7))
        colors = [self.emotion_colors.get(e, "#000000") for e in emotions_data.keys()]
        bars = plt.bar(emotions_data.keys(), [emotions_data[e] for e in emotions_data.keys()], color=colors)
        plt.ylabel('Confidence Score (%)', fontsize=16)
        plt.xticks(rotation=45, fontsize=14)
        plt.ylim(0, 100)
        for i, v in enumerate(emotions_data.values()):
            plt.text(i, v+1, f'{v:.1f}%', ha='center', va='bottom', fontsize=14)
        plt.tight_layout()
        return plt

    def display_demographics(self, results):
        """Display Age and Gender Distribution charts vertically with separators"""
        st.markdown("### 🎂 Age Distribution")
        fig_age = plt.figure(figsize=(14, 7))
        ages = [face['age'] for face in results]
        plt.hist(ages, bins=range(0, 101, 10), edgecolor='black', alpha=0.7)
        plt.xlabel('Age Range', fontsize=16)
        plt.ylabel('Count', fontsize=16)
        plt.xticks(range(0, 101, 10), [f"{i}-{i+10}" for i in range(0, 101, 10)], fontsize=14)
        plt.tight_layout()
        st.pyplot(fig_age)
        st.markdown("---")
        st.markdown("### 👤 Gender Distribution")
        fig_gender = plt.figure(figsize=(14, 7))
        genders = [max(face['gender'], key=face['gender'].get) for face in results]
        gender_counts = {'Man': genders.count('Man'), 'Woman': genders.count('Woman')}
        plt.pie(gender_counts.values(), labels=gender_counts.keys(),
                autopct='%1.1f%%', colors=['#4B77BE', '#F27999'], textprops={'fontsize': 14})
        plt.tight_layout()
        st.pyplot(fig_gender)

    def display_results(self, results, img_rgb):
        """Display individual face analysis cards with emoji labels and full face (with margin)"""
        st.markdown("### 👥 Individual Face Analysis")
        st.markdown(textwrap.dedent("""\
            <style>
                .face-container {
                    display: flex;
                    overflow-x: auto;
                    padding: 20px 0;
                    gap: 15px;
                }
                .face-card {
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    min-width: 280px;
                    padding: 15px;
                    transition: transform 0.2s;
                }
                .face-card:hover {
                    transform: translateY(-5px);
                }
                .face-image {
                    border-radius: 8px;
                    width: 100%;
                    height: 200px;
                    object-fit: cover;
                }
            </style>
        """), unsafe_allow_html=True)
        container_html = "<div class='face-container'>"
        for idx, face in enumerate(results):
            emotion_color = self.emotion_colors[max(face['emotion'], key=face['emotion'].get)]
            x, y, w, h = face['region'].values()
            # Increase margin to 20% of face width to show full face
            margin = int(0.2 * w)
            new_x = max(0, x - margin)
            new_y = max(0, y - margin)
            new_w = min(img_rgb.shape[1] - new_x, w + 2 * margin)
            new_h = min(img_rgb.shape[0] - new_y, h + 2 * margin)
            face_img = img_rgb[new_y:new_y+new_h, new_x:new_x+new_w]
            buffered = BytesIO()
            Image.fromarray(face_img).save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            face_card = textwrap.dedent(f"""\
                <div class="face-card" style="border: 3px solid {emotion_color};">
                    <h4 style="margin: 0 0 0.5rem 0; color: #2A2A2A;">Person {idx + 1}</h4>
                    <img src="data:image/jpeg;base64,{img_str}" class="face-image">
                    <div style="padding: 0 0.5rem;">
                        <p style="margin: 0.3rem 0; font-size: 0.95rem;">
                            <span style="color: #666; font-weight: 500;">🎂 Age:</span> 
                            <span style="color: #2A2A2A;">{self.get_age_range(face['age'])}</span>
                        </p>
                        <p style="margin: 0.3rem 0; font-size: 0.95rem;">
                            <span style="color: #666; font-weight: 500;">👤 Gender:</span> 
                            <span style="color: #2A2A2A;">{face['dominant_gender']}</span>
                        </p>
                        <p style="margin: 0.3rem 0; font-size: 0.95rem;">
                            <span style="color: #666; font-weight: 500;">😃 Emotion:</span> 
                            <span style="color: {emotion_color}; font-weight: 600;">{max(face['emotion'], key=face['emotion'].get)}</span>
                        </p>
                        <p style="margin: 0.3rem 0; font-size: 0.95rem;">
                            <span style="color: #666; font-weight: 500;">🌍 Ethnicity:</span> 
                            <span style="color: #2A2A2A; font-weight: 600;">{face['dominant_race']}</span>
                        </p>
                    </div>
                </div>
            """)
            container_html += face_card
        container_html += "</div>"
        st.markdown(container_html, unsafe_allow_html=True)

    def get_age_range(self, age):
        base = (age // 5) * 5
        return f"{base}-{base + 5}"

    def run(self):
        st.markdown("#### Upload an image to analyze facial features and emotional states")
        
        # Image Module Expander
        with st.expander("ℹ️ About this module", expanded=False):
            st.markdown(textwrap.dedent("""\
                <div style="padding:15px; border-radius:10px; background:#f8f9fa;">
                  <h3 style="color:#4CAF50; margin-bottom:15px;">See Beyond the Smiles 😊😠😲</h3>
                  ✨ <strong>What facial analysis reveals</strong>:
                  <div style="margin-left:20px; margin-top:10px;">
                    <br>🔹 <strong>Group Insights</strong><br>
                    - Age distribution analysis<br>
                    - Gender balance overview<br>
                    - Dominant emotions<br><br>
                    🔹 <strong>Individual Breakdown</strong><br>
                    - Personal emotion intensity<br>
                    - Confidence level estimates<br>
                    - Attention hotspots<br><br>
                    🔹 <strong>Visual Storytelling</strong><br>
                    - Emotional group map<br>
                    - Reaction comparisons<br>
                    - Demographic patterns
                  </div>
                  <p style="margin-top:15px; color:#666; font-style:italic;">
                  Great for event photos, team pictures, or audience analysis!
                  </p>
                </div>
            """), unsafe_allow_html=True)
            
        # Image Source Selection: Upload or Select Sample Image
        input_method = st.radio(
            "Select Image Source",
            ("Upload Image", "Select Sample Image"),
            help="Select 'Upload Image' to upload your own image or 'Select Sample Image' to choose from sample images"
        )
        img_rgb = None
        if input_method == "Upload Image":
            uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            sample_dir = r"C:\Users\HARSHAL\OneDrive\Desktop\New folder\SENTIME\sample_images"
            if os.path.exists(sample_dir):
                sample_files = [f for f in os.listdir(sample_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if sample_files:
                    sample_choice = st.selectbox("Choose a sample image", sample_files)
                    if sample_choice:
                        img = Image.open(os.path.join(sample_dir, sample_choice)).convert('RGB')
                        img_rgb = np.array(img)
                else:
                    st.error("No sample images found in the sample_images folder.")
            else:
                st.error("The sample_images folder does not exist.")
        
        if img_rgb is None:
            st.info("Please upload an image or select a sample image.")
            return

        with st.spinner("Analyzing facial features..."):
            faces = self.detect_faces(img_rgb)
            results = self.analyze_faces(img_rgb, faces)
            if not results:
                st.error("The image does not contain any person. Please upload an image containing people.")
                return

        st.image(self.draw_faces(img_rgb, results), use_column_width=True, 
                 caption="Analyzed Image with Emotion Detection")
        st.markdown("### 📈 Analysis Summary")
        summary_cols = st.columns(2)
        with summary_cols[0]:
            st.markdown(f"""
                <div class='summary-card'>
                    <h3 style='margin: 0 0 0.5rem 0; color: #666;'>Total Faces</h3>
                    <div style='font-size: 2rem; color: #2A2A2A; font-weight: 700;'>{len(results)}</div>
                </div>
            """, unsafe_allow_html=True)
        with summary_cols[1]:
            dominant_emotions = [max(face['emotion'], key=face['emotion'].get) for face in results]
            dominant_emotion = max(set(dominant_emotions), key=dominant_emotions.count)
            avg_conf = sum(face['emotion'][dominant_emotion] for face in results) / len(results)
            st.markdown(f"""
                <div class='summary-card'>
                    <h3 style='margin: 0 0 0.5rem 0; color: #666;'>Dominant Emotion</h3>
                    <div style='font-size: 1.5rem; color: {self.emotion_colors[dominant_emotion]}; font-weight: 700;'>
                        {dominant_emotion.capitalize()}
                    </div>
                    <div style='font-size: 0.9rem; color: #666;'>Avg. Confidence: {avg_conf:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 📊 Detailed Emotion Distribution")
        plt_obj = self.create_emotion_chart(results)
        st.pyplot(plt_obj)
        st.markdown("---")
        self.display_demographics(results)
        st.markdown("---")
        self.display_results(results, img_rgb)

def main():
    st.set_page_config(page_title="Face Sentiment Analyzer", layout="wide")
    app = ImageSentimentModule()
    app.run()

if __name__ == "__main__":
    main()


