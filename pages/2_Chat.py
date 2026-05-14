# pages/2_Chat.py — Employee Q&A Interface
import streamlit as st
from core.pipeline import query_department
from core.store import store
from core.config import cfg
from utils.ui import inject_custom_css

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

# Inject custom styles
inject_custom_css()

# ── Sidebar: Department & Settings ────────────────────────────────────
with st.sidebar:
    st.markdown("<h1 style='font-size: 1.5rem;'>🏢 Access Control</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Select your department to access authorized knowledge.</p>", unsafe_allow_html=True)

    department = st.selectbox(
        "Your Department",
        cfg.departments,
        format_func=lambda x: x.upper(),
        help="You can ONLY access documents from this department.",
        label_visibility="collapsed"
    )

    st.markdown(
        f'<div style="background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 0.5rem 1rem; border-radius: 12px; font-size: 0.85rem; font-weight: 700; text-align: center; margin-top: 1rem;">🔒 {department.upper()} ACCESS GRANTED</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    with st.expander("⚙️ Inference Settings"):
        model = st.selectbox("LLM Model", cfg.available_models)
        top_k = st.slider("Context chunks", min_value=3, max_value=15, value=cfg.top_k)

    st.divider()

    # Show indexed sources for this department
    sources = store.list_sources(department)
    if sources:
        st.markdown(f"### 📄 Authorized Files ({len(sources)})")
        for s in sources:
            st.markdown(f"<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.3rem;'>• {s}</div>", unsafe_allow_html=True)
    else:
        st.warning(
            f"No documents indexed for **{department.upper()}**."
        )

    st.divider()
    st.caption(f"Status: Connected to Local RAG")

# ── Main Chat Area ────────────────────────────────────────────────────
st.markdown(f"<h1>💬 {department.upper()} Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #94a3b8;'>Querying departmental knowledge base with zero cloud dependency.</p>", unsafe_allow_html=True)

# ── Session state for chat history ────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_dept" not in st.session_state:
    st.session_state.active_dept = department

# Clear chat when department changes
if st.session_state.active_dept != department:
    st.session_state.messages = []
    st.session_state.active_dept = department

# Render existing messages
for msg in st.session_state.messages:
    avatar = "data/logo.png" if msg["role"] == "assistant" else "data/user_avatar.png"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if "metadata" in msg and msg["metadata"]:
            st.caption(msg["metadata"])

# ── Chat Input ────────────────────────────────────────────────────────
if prompt := st.chat_input(f"Ask about {department.upper()} documents..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="data/user_avatar.png"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="data/logo.png"):
        if store.is_empty(department):
            answer = (
                f"⚠️ There are no documents indexed for the **{department.upper()}** department yet. "
                f"Please contact an Admin to upload relevant materials."
            )
            st.warning(answer)
            metadata_str = ""
        else:
            with st.spinner("🔍 Analyzing documents..."):
                try:
                    result = query_department(
                        question=prompt,
                        department=department,
                        model=model,
                        top_k=top_k,
                    )

                    answer = result["answer"]
                    st.markdown(answer)

                    # Metadata bar
                    metadata_str = (
                        f"⏱ {result['latency_ms']}ms · "
                        f"🤖 {result['model']} · "
                        f"📄 {len(result['chunks'])} sources"
                    )
                    st.caption(metadata_str)

                    # Expandable source chunks
                    with st.expander("🔍 View Grounding Sources"):
                        for i, chunk in enumerate(result["chunks"], 1):
                            st.markdown(f"**Source {i}:** `{chunk['source']}` (Relevance: `{chunk['score']:.2f}`)")
                            st.markdown(f"""
                            <div style='background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px; font-size: 0.9rem; border-left: 2px solid var(--primary); margin-top: 0.5rem;'>
                                {chunk['text']}
                            </div>
                            """, unsafe_allow_html=True)
                            if i < len(result["chunks"]):
                                st.markdown("<br>", unsafe_allow_html=True)

                except Exception as e:
                    answer = f"❌ Error: {str(e)}"
                    st.error(answer)
                    metadata_str = ""

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "metadata": metadata_str if metadata_str else None,
        })
