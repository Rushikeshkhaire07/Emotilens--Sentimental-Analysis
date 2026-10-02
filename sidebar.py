import streamlit as st
import os

def setup_sidebar():
    st.markdown("""
        <style>
            /* Sidebar container styling */
            section[data-testid="stSidebar"] {
                background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                padding: 1.5rem 1rem;
                border-right: 1px solid #dee2e6;
            }
            
            /* Sidebar header styling */
            .sidebar-header {
                text-align: left;
                color: #1f77b4;
                padding: 0.5rem 0;
                margin-bottom: 1rem;
                border-bottom: 2px solid #dee2e6;
                font-size: 1.3rem;
                font-weight: 600;
            }
            
            /* Selectbox styling */
            div[data-testid="stSelectbox"] {
                margin: 1rem 0;
            }
            div[data-testid="stSelectbox"] select {
                background-color: #fff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 0.7rem 1rem;
                font-size: 1rem;
                font-weight: 500;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            }
            
            /* Fixed footer styling */
            .sidebar-footer {
                position: fixed;
                bottom: 0;
                left: 0;
                padding: 1rem;
                font-size: 0.8rem;
                color: #666;
                border-top: 1px solid #dee2e6;
                width: 100%;
                background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar header
    st.sidebar.markdown("""
        <div class="sidebar-header">
            🎯 Analysis Modules
        </div>
    """, unsafe_allow_html=True)
    
    # Dictionary for module icons
    modules = {
        "Home": "🏠",
        "Text Sentiment": "📝",
        "Image Sentiment": "🖼️",
        "X/Twitter Analysis": "🐦",
        "WhatsApp Chat Sentiment": "💬"
    }
    
    # Create selectbox options with icons
    options = [f"{icon} {module}" for module, icon in modules.items()]
    
    selected = st.sidebar.selectbox("Select a module", options, index=0, key="module_selector")
    
   
    
    # Return only the module name (icon removed)
    return selected.split(" ", 1)[1]

# Example usage in your app:
if __name__ == "__main__":
    selected_module = setup_sidebar()
    st.write("Selected Module:", selected_module)
