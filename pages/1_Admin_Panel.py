# pages/1_Admin_Panel.py — Document Management
import streamlit as st
from core.pipeline import index_documents
from core.store import store
from core.config import cfg
from utils.pdf_parser import extract_pdf_text
from utils.ui import inject_custom_css
import json

st.set_page_config(page_title="Admin Panel", page_icon="data/logo.png", layout="wide")

# Inject custom styles
inject_custom_css()

st.title("🔑 Admin Control Center")
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Orchestrate your local knowledge base and manage departmental data isolation.</p>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────
tab_upload, tab_manage, tab_stats = st.tabs([
    "📥 Ingest Knowledge",
    "🗂️ Knowledge Inventory",
    "📊 System Analytics",
])

# ━━ Tab 1: Upload ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_upload:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_dept, col_files = st.columns([1, 2])

    with col_dept:
        st.markdown("### 🏷️ Target Department")
        department = st.selectbox(
            "Select Destination",
            [d.upper() for d in cfg.departments],
            help="Documents will be tagged with this department for ABAC isolation.",
            label_visibility="collapsed"
        )
        st.info(f"Indexing to: **{department}**")

    with col_files:
        st.markdown("### 📄 Document Upload")
        files = st.file_uploader(
            "Upload Files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            help="You can upload multiple files at once.",
            label_visibility="collapsed"
        )

    if st.button("🚀 Start Indexing Pipeline", type="primary", disabled=not files, use_container_width=True):
        dept_lower = department.lower()
        progress_bar = st.progress(0)
        status = st.empty()

        for i, f in enumerate(files):
            status.info(f"Processing {f.name}...")

            # Extract text
            if f.name.lower().endswith(".pdf"):
                text = extract_pdf_text(f.read())
            else:
                raw = f.read()
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    text = raw.decode("latin-1")

            if not text.strip():
                st.warning(f"⚠️ {f.name} — no text extracted, skipping.")
                continue

            # Index
            n = index_documents(text, department=dept_lower, source=f.name)
            st.success(f"✅ **{f.name}** → {n} chunks indexed under **{department}**")

            progress_bar.progress((i + 1) / len(files))

        status.empty()
        progress_bar.empty()
        st.balloons()

    st.divider()
    with st.expander("🧩 Advanced: Structured JSON Ingestion"):
        st.caption("Paste JSON containing `department`, `title` (optional), and `content` fields.")
        
        json_input = st.text_area(
            "Paste JSON here", 
            height=200, 
            placeholder='[\n  {\n    "id": "management_001",\n    "department": "MANAGEMENT",\n    "title": "Strategic Goals 2025",\n    "content": "The company\'s strategic priorities..."\n  }\n]'
        )
        
        if st.button("📥 Process JSON Data", disabled=not json_input.strip(), use_container_width=True):
            try:
                data = json.loads(json_input)
                if isinstance(data, dict):
                    data = [data]
                    
                if not isinstance(data, list):
                    st.error("JSON must be an object or an array of objects.")
                else:
                    progress_bar = st.progress(0)
                    status = st.empty()
                    success_count = 0
                    
                    for i, item in enumerate(data):
                        dept = str(item.get("department", "")).lower().strip()
                        title = str(item.get("title", item.get("id", f"json_doc_{i}")))
                        content = str(item.get("content", ""))
                        
                        status.info(f"Processing {title}...")
                        
                        if not dept:
                            st.warning(f"⚠️ **{title}** — missing 'department', skipping.")
                            continue
                        if not content.strip():
                            st.warning(f"⚠️ **{title}** — missing 'content', skipping.")
                            continue
                            
                        n = index_documents(content, department=dept, source=title)
                        st.success(f"✅ **{title}** → {n} chunks indexed under **{dept.upper()}**")
                        success_count += 1
                        
                        progress_bar.progress((i + 1) / len(data))
                        
                    status.empty()
                    progress_bar.empty()
                    if success_count > 0:
                        st.balloons()
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")

# ━━ Tab 2: Manage ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_manage:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📂 Managed Departments")

    has_any = False
    for dept in cfg.departments:
        sources = store.list_sources(dept)
        if not sources:
            continue
        has_any = True

        with st.expander(f"📦 **{dept.upper()}** — {len(sources)} active document(s)"):
            for src in sources:
                col_name, col_del = st.columns([5, 1])
                col_name.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 8px; border-left: 3px solid var(--primary);'>
                    📄 {src}
                </div>
                """, unsafe_allow_html=True)
                if col_del.button("🗑️ Remove", key=f"del_{dept}_{src}", use_container_width=True):
                    store.delete_source(dept, src)
                    st.success(f"Deleted '{src}'")
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"🧨 Wipe {dept.upper()} Knowledge Base", key=f"del_all_{dept}"):
                store.delete_department(dept)
                st.warning(f"All documents for {dept.upper()} have been deleted.")
                st.rerun()

    if not has_any:
        st.info("No documents indexed yet. Start by uploading files in the Ingest tab.")

# ━━ Tab 3: Dashboard ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_stats:
    st.markdown("<br>", unsafe_allow_html=True)
    stats = store.get_stats()

    if stats:
        total_chunks = sum(stats.values())
        total_depts = len(stats)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Indexed Chunks", f"{total_chunks:,}")
        with m2:
            st.metric("Active Departments", total_depts)
        with m3:
            st.metric("Embedding Dims", cfg.embed_dimensions)

        st.divider()

        import pandas as pd
        df = pd.DataFrame(
            [{"Department": k.upper(), "Chunks": v} for k, v in stats.items()]
        ).sort_values("Chunks", ascending=False)

        col_chart, col_table = st.columns([2, 1])
        
        with col_chart:
            st.markdown("### 📈 Distribution by Department")
            st.bar_chart(df.set_index("Department"), color="#6366f1")

        with col_table:
            st.markdown("### 📋 Raw Statistics")
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("The knowledge base is currently empty.")

    st.divider()
    st.caption(f"Engine: `{cfg.embed_model}` · Architecture: {cfg.embed_dimensions} (MRL) · Storage: LanceDB")
