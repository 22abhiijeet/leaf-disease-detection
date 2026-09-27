import streamlit as st
import base64
import sys
from pathlib import Path

# Add Leaf Disease directory to path
sys.path.insert(0, str(Path(__file__).parent / "Leaf Disease"))
try:
    from main import LeafDiseaseDetector
except ImportError:
    pass

st.set_page_config(page_title="Leaf Disease Detection", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e3f2fd 0%, #f7f9fa 100%); }
    .result-card { background: rgba(255,255,255,0.95); border-radius: 18px; box-shadow: 0 4px 24px rgba(44,62,80,0.10); padding: 2.5em 2em; margin: 1.5em 0; }
    .disease-title { color: #1b5e20; font-size: 2.2em; font-weight: 700; margin-bottom: 0.5em; }
    .section-title { color: #1976d2; font-size: 1.25em; margin-top: 1.2em; font-weight: 600; }
    .timestamp { color: #616161; font-size: 0.95em; margin-top: 1.2em; text-align: right; }
    .info-badge { display: inline-block; background: #e3f2fd; color: #1976d2; border-radius: 8px; padding: 0.3em 0.8em; margin-right: 0.5em; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-top: 1em;'>
        <span style='font-size:2.5em;'>🌿</span>
        <h1 style='color: #1565c0; margin-bottom:0;'>Leaf Disease Detection</h1>
        <p style='color: #616161; font-size:1.15em;'>Upload a leaf image to detect diseases and get expert recommendations.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Preview")

with col2:
    if uploaded_file and st.button("🔍 Detect Disease", use_container_width=True):
        with st.spinner("Analyzing image using Groq AI..."):
            try:
                base64_str = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                detector = LeafDiseaseDetector()
                res = detector.analyze_leaf_image_base64(base64_str)

                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    if res.get("disease_type") == "invalid_image":
                        st.markdown("<div class='disease-title'>⚠️ Invalid Image</div>", unsafe_allow_html=True)
                        st.write("Please upload a clear plant leaf image.")
                    elif res.get("disease_detected"):
                        st.markdown(f"<div class='disease-title'>🦠 {res.get('disease_name', 'N/A')}</div>", unsafe_allow_html=True)
                        st.markdown(f"<span class='info-badge'>Type: {res.get('disease_type', 'N/A')}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span class='info-badge'>Severity: {res.get('severity', 'N/A')}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span class='info-badge'>Confidence: {res.get('confidence', 'N/A')}%</span>", unsafe_allow_html=True)
                        
                        st.markdown("<div class='section-title'>Symptoms</div>", unsafe_allow_html=True)
                        st.markdown("<ul>" + "".join([f"<li>{s}</li>" for s in res.get("symptoms", [])]) + "</ul>", unsafe_allow_html=True)
                        
                        st.markdown("<div class='section-title'>Treatment</div>", unsafe_allow_html=True)
                        st.markdown("<ul>" + "".join([f"<li>{t}</li>" for t in res.get("treatment", [])]) + "</ul>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='disease-title'>✅ Healthy Leaf</div>", unsafe_allow_html=True)
                        st.write("No disease detected!")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("Failed to analyze image.")
            except Exception as e:
                st.error(f"Error: {str(e)}")