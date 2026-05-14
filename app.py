# app.py — Enterprise RAG Home Page
import streamlit as st
from utils.ui import inject_custom_css, hero_section, card

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="data/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom styles
inject_custom_css()

# ── Hero ──────────────────────────────────────────────────────────────
hero_section(
    "🏢 Enterprise Knowledge AI",
    "Secure, local-first document intelligence with department-level data isolation and sub-2s response times."
)

col_logo, col_main = st.columns([1, 8])
with col_logo:
    st.image("data/logo.png", width=120)
with col_main:
    st.markdown("<br>", unsafe_allow_html=True)

# ── Role Selection ────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, spacer, col2 = st.columns([1, 0.2, 1])

with col1:
    st.markdown(card("💬", "Employee Chat", "Ask questions about your department's documents. AI answers are grounded in your specific indexed knowledge base."), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Open Chat Interface", use_container_width=True, key="btn_chat"):
        st.switch_page("pages/2_Chat.py")

with col2:
    st.markdown(card("🔑", "Admin Control", "Upload new documents, manage department access, and monitor the health of your local vector database."), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Open Management Panel", use_container_width=True, key="btn_admin"):
        st.switch_page("pages/1_Admin_Panel.py")

# ── Features ──────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Built for Security & Performance</h2>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔒</div>
        <h4 style='margin-bottom: 0.5rem;'>Zero Trust Access</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>ABAC ensures users only see data from their authorized departments.</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚡</div>
        <h4 style='margin-bottom: 0.5rem;'>Hardware Accelerated</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>Optimized for local GPUs (RTX 3050+) with sub-2s query latency.</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🧠</div>
        <h4 style='margin-bottom: 0.5rem;'>Hybrid Intelligence</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>Combines semantic vector search with keyword-based BM25 retrieval.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
f4, f5, f6 = st.columns(3)
with f4:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💾</div>
        <h4 style='margin-bottom: 0.5rem;'>Persistent Memory</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>LanceDB provides high-performance, persistent storage for millions of vectors.</p>
    </div>
    """, unsafe_allow_html=True)

with f5:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🖥️</div>
        <h4 style='margin-bottom: 0.5rem;'>100% Private</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>No data leaves your infrastructure. Fully compatible with Ollama.</p>
    </div>
    """, unsafe_allow_html=True)

with f6:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📄</div>
        <h4 style='margin-bottom: 0.5rem;'>Multi-format</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>Native support for PDF, TXT, and structured JSON ingestion.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.caption("Enterprise RAG · Powered by Ollama + LanceDB + Nomic · Running on Local Infrastructure")
