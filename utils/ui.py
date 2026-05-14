# utils/ui.py - UI Helpers for Streamlit
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@400;600&display=swap');

        :root {
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.5);
            --secondary: #a855f7;
            --background: #0f172a;
            --surface: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --glass: rgba(30, 41, 59, 0.7);
            --border: rgba(255, 255, 255, 0.1);
        }

        .stApp {
            background-color: var(--background);
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3, .hero-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
        }

        /* Glassmorphism Card */
        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .glass-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 var(--primary-glow);
        }

        /* Animated Background */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 10% 20%, rgba(168, 85, 247, 0.05) 0%, transparent 40%);
            z-index: -1;
        }

        /* Buttons Styling */
        .stButton>button {
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s ease;
            border: none;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white !important;
        }

        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 20px var(--primary-glow);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0b1120;
            border-right: 1px solid var(--border);
        }

        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre;
            background-color: transparent;
            border-radius: 4px 4px 0 0;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 600;
            color: var(--text-muted);
        }

        .stTabs [aria-selected="true"] {
            color: var(--primary) !important;
            border-bottom-color: var(--primary) !important;
        }

        /* Metric Styling */
        [data-testid="stMetricValue"] {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Chat Input Styling */
        .stChatInputContainer {
            padding-bottom: 20px;
        }

        /* Hide Streamlit Header/Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
    </style>
    """, unsafe_allow_html=True)

def hero_section(title, subtitle):
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 3rem 0;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {title}
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; max-width: 600px; margin: 0 auto;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)

def card(icon, title, text):
    return f"""
    <div class="glass-card">
        <div style="font-size: 3rem; margin-bottom: 1.5rem;">{icon}</div>
        <h3 style="margin-bottom: 1rem; color: #f8fafc;">{title}</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">{text}</p>
    </div>
    """
