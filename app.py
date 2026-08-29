"""
Pre-University Biology AI Tutor - Modern Dark-Themed Conversational RAG UI
Built with Streamlit, LangChain, LangGraph, ChromaDB & Ollama.
"""

import importlib
import streamlit as st
import time
import json
from pathlib import Path
import requests

import src.agent_graph
importlib.reload(src.agent_graph)
from src.config import CORPUS_DIR, OLLAMA_MODEL, EMBEDDING_MODEL_NAME, OLLAMA_BASE_URL
from src.agent_graph import ask_question, reset_retriever
from src.ingestion import run_ingestion
from src.hybrid_retriever import HybridRetriever

def fetch_local_models():
    """Robust fetcher for local Ollama models."""
    try:
        res = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if res.status_code == 200:
            models = [m["name"] for m in res.json().get("models", [])]
            if models:
                return models
    except Exception:
        pass
    return [OLLAMA_MODEL, "muse-glimmer-30b:latest", "llama3.2:latest"]

# Page Setup
st.set_page_config(
    page_title="Pre-University Biology AI Tutor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F8FAFC;
    }
    
    /* Header Gradient Dark Card */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #064E3B 100%);
        color: #F8FAFC;
        padding: 30px 34px;
        border-radius: 20px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.6);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-top: 8px;
        margin-bottom: 16px;
        line-height: 1.5;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.12);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #34D399;
        margin-right: 8px;
        margin-bottom: 6px;
        border: 1px solid rgba(52, 211, 153, 0.25);
    }
    
    /* Quick Prompt Section */
    .prompt-section-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #94A3B8;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    
    /* Citation Cards (Modern Grid & Frosted Glass) */
    .citation-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-top: 3px solid #10B981;
        padding: 14px 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .citation-card:hover {
        border-color: #374151;
        transform: translateY(-2px);
    }
    .citation-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .citation-badge {
        font-size: 0.82rem;
        font-weight: 700;
        color: #34D399;
        background: rgba(16, 185, 129, 0.12);
        padding: 3px 10px;
        border-radius: 6px;
        border: 1px solid rgba(52, 211, 153, 0.2);
    }
    .citation-link {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8 !important;
        text-decoration: none !important;
        background: rgba(255, 255, 255, 0.05);
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.2s ease;
    }
    .citation-link:hover {
        color: #10B981 !important;
        border-color: #10B981;
        background: rgba(16, 185, 129, 0.1);
    }
    .citation-section {
        font-size: 0.82rem;
        font-weight: 600;
        color: #CBD5E1;
        margin-bottom: 8px;
    }
    .citation-quote {
        color: #9CA3AF;
        font-size: 0.82rem;
        font-style: italic;
        line-height: 1.45;
        background: #0F172A;
        padding: 8px 12px;
        border-radius: 8px;
        border-left: 3px solid #3B82F6;
    }
    
    /* Buttons in Dark Mode */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #334155;
        background-color: #1E293B;
        color: #F1F5F9;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        border-color: #10B981;
        color: #10B981;
        background-color: #0F172A;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.15);
    }
    
    /* Chat message container */
    .stChatMessage {
        background-color: transparent !important;
        padding: 14px 0px;
    }
    
    /* Sidebar chapter links */
    .sidebar-chapter-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 7px 10px;
        margin-bottom: 6px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        color: #E2E8F0 !important;
        text-decoration: none !important;
        font-size: 0.83rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .sidebar-chapter-link:hover {
        background: rgba(16, 185, 129, 0.14);
        border-color: #10B981;
        color: #34D399 !important;
        transform: translateX(3px);
    }
    .sidebar-chapter-icon {
        font-size: 0.78rem;
        color: #64748B;
    }
    .sidebar-chapter-link:hover .sidebar-chapter-icon {
        color: #34D399;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0A0F1D;
        border-right: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome! I am your Pre-University Biology AI Tutor.**\n\n"
                "I am strictly grounded in all **12 official textbook chapters** from **preuniversity.grkraj.org** "
                "(authored by Prof. Dr. G. R. Kantharaj). You can freely type any conceptual question in the chat bar below, "
                "or click any of the suggested topic chips to get started!"
            ),
            "citations": [],
            "latency": None
        }
    ]

if "queued_query" not in st.session_state:
    st.session_state.queued_query = None

# Sidebar Content
with st.sidebar:
    st.markdown("### 🌿 Biology Tutor Studio")
    st.caption("100% Local Agentic RAG • LangChain & LangGraph")
    
    st.divider()
    st.markdown("#### ⚙️ Pipeline & Model Selection")
    
    available_models = fetch_local_models()
    default_idx = 0
    if OLLAMA_MODEL in available_models:
        default_idx = available_models.index(OLLAMA_MODEL)
    elif "muse-glimmer-30b:latest" in available_models:
        default_idx = available_models.index("muse-glimmer-30b:latest")
        
    selected_model = st.selectbox(
        "🤖 Active Ollama Model:",
        options=available_models,
        index=default_idx,
        help="Choose which locally installed Ollama model to use for answering questions"
    )
    
    st.caption(f"⚡ Currently using: `{selected_model}`")
    st.markdown(f"**Embeddings:** `{EMBEDDING_MODEL_NAME.split('/')[-1]}`")
    st.markdown("**Retrieval:** `Dense ChromaDB + Sparse BM25 (RRF)`")
    st.markdown("**Guardrails:** `Relevance Grading + Anti-Hallucination`")
    st.markdown("**Knowledge Base:** `12 Pre-University Chapters`")
    
    st.divider()
    st.markdown("#### 📚 12 Indexed Chapters")
    st.caption("Click to view source lecture notes on website:")
    chapters = sorted(list(CORPUS_DIR.glob("*.md")))
    for ch in chapters:
        chapter_name = ch.stem.replace("Chapter_", "Ch. ").replace("_", " ")
        chapter_url = "https://grkraj.org/pre-university/"
        st.markdown(
            f'<a class="sidebar-chapter-link" href="{chapter_url}" target="_blank" rel="noopener noreferrer">'
            f'<span>📖 {chapter_name}</span><span class="sidebar-chapter-icon">↗</span></a>',
            unsafe_allow_html=True
        )
        
    st.divider()
    col_reindex, col_clear = st.columns(2)
    with col_reindex:
        if st.button("🔄 Sync Docs", use_container_width=True, help="Re-index vector store and BM25 index"):
            with st.spinner("Indexing all 12 chapters..."):
                run_ingestion()
                reset_retriever()
                st.toast("12 chapters successfully indexed!", icon="✅")
                st.rerun()
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True, help="Reset conversation history"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. How can I assist you with your pre-university biology studies?",
                    "citations": [],
                    "latency": None
                }
            ]
            st.rerun()

    # Chat Export Option
    if len(st.session_state.messages) > 1:
        chat_export_json = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            label="📥 Export Chat History",
            data=chat_export_json,
            file_name="biology_rag_chat.json",
            mime="application/json",
            use_container_width=True
        )

# Helper to render clean, professional citation cards
def render_citations_ui(citations: list, expanded: bool = False):
    if not citations:
        return
    with st.expander(f"📚 Verified Sources & Literature Citations ({len(citations)})", expanded=expanded):
        cols = st.columns(2)
        for i, c in enumerate(citations):
            col = cols[i % 2]
            with col:
                source_title = c.get("source", "Chapter")
                section_title = c.get("section", "General")
                snippet = c.get("snippet", "")
                url = c.get("url", "https://grkraj.org/pre-university/")
                
                card_html = f"""
                <div class="citation-card">
                    <div class="citation-header">
                        <span class="citation-badge">[{i+1}] {source_title}</span>
                        <a class="citation-link" href="{url}" target="_blank" rel="noopener noreferrer">↗ Website</a>
                    </div>
                    <div class="citation-section">📌 <i>Section: {section_title}</i></div>
                    <div class="citation-quote">"{snippet}"</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

# Main Header Banner (Dark Modern Card)
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">
        <span>🌿 Pre-University Biology AI Tutor</span>
    </div>
    <div class="hero-subtitle">
        100% Local Conversational Assistant grounded in all 12 textbook chapters from <b>preuniversity.grkraj.org</b>
    </div>
    <div>
        <span class="badge-pill">⚡ LangGraph State Machine</span>
        <span class="badge-pill">🔍 Hybrid BM25 + Chroma Search</span>
        <span class="badge-pill">🛡️ Strict Factual Grounding</span>
        <span class="badge-pill">📖 12 Verified Chapters</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_explorer, tab_retriever_debug = st.tabs([
    "💬 Interactive Chat",
    "📖 12 Chapters Explorer",
    "🔍 Search & Retrieval Inspector"
])

# -------------------------------------------------------------
# TAB 1: INTERACTIVE CHAT
# -------------------------------------------------------------
with tab_chat:
    # Quick Sample Questions Section
    st.markdown('<div class="prompt-section-title">💡 Quick Suggested Questions Across Curriculum</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔬 Stomata & Guard Cells", use_container_width=True, help="Plant Anatomy"):
            st.session_state.queued_query = "How do guard cells regulate the opening and closing of stomata?"
            st.rerun()
    with col2:
        if st.button("☀️ Calvin Cycle (C3)", use_container_width=True, help="Photosynthesis"):
            st.session_state.queued_query = "Explain the three main phases of the Calvin Cycle (C3 pathway) in photosynthesis."
            st.rerun()
    with col3:
        if st.button("💧 Cohesion-Tension Pull", use_container_width=True, help="Water Relations"):
            st.session_state.queued_query = "Explain the Cohesion-Tension-Transpiration Pull Theory for water movement in xylem."
            st.rerun()
    with col4:
        if st.button("🧬 Mendel's 9:3:3:1 Ratio", use_container_width=True, help="Genetics"):
            st.session_state.queued_query = "What is Mendel's Law of Independent Assortment and explain the 9:3:3:1 dihybrid ratio?"
            st.rerun()

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("🌱 Mineral Criteria (Arnon)", use_container_width=True, help="Mineral Nutrition"):
            st.session_state.queued_query = "What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout?"
            st.rerun()
    with col6:
        if st.button("⚡ Respiration & ETS", use_container_width=True, help="Bioenergetics"):
            st.session_state.queued_query = "How does oxidative phosphorylation in mitochondrial cristae generate ATP via chemiosmosis?"
            st.rerun()
    with col7:
        if st.button("🍇 Phytohormones (Auxin/ABA)", use_container_width=True, help="Plant Growth"):
            st.session_state.queued_query = "Compare the functions of Auxins in apical dominance with Abscisic Acid (ABA) in drought stress."
            st.rerun()
    with col8:
        if st.button("🧪 DNA Double Helix (Watson-Crick)", use_container_width=True, help="Molecular Genetics"):
            st.session_state.queued_query = "Explain the structural features of the Watson-Crick B-DNA double helix model."
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Conversation History
    for message in st.session_state.messages:
        role = message["role"]
        avatar = "👤" if role == "user" else "🌿"
        
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])
            
            # Show latency badge if available
            if message.get("latency"):
                st.caption(f"⏱️ *Generated in {message['latency']}s via local LangGraph pipeline.*")
                
            # Render Clean Professional Citations
            if message.get("citations"):
                render_citations_ui(message["citations"], expanded=False)

    # Top-Level Chat Input (Always Active & Ready to Type)
    user_typed_input = st.chat_input("Type any biology question here (e.g., 'What is the role of the Casparian strip?')...")

    # Determine query to process (either typed by user or clicked from quick prompts)
    active_query = None
    if user_typed_input:
        active_query = user_typed_input
    elif st.session_state.queued_query:
        active_query = st.session_state.queued_query
        st.session_state.queued_query = None

    # Execute RAG Pipeline on Query
    if active_query:
        # Display User Question
        st.session_state.messages.append({"role": "user", "content": active_query, "citations": [], "latency": None})
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_query)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🌿"):
            status_container = st.status("🧠 Analyzing textbook chapters with LangGraph...", expanded=True)
            
            with status_container:
                st.write("🔍 Running Hybrid Retrieval (Dense Chroma + Sparse BM25)...")
                start_time = time.time()
                
                st.write("⚖️ Grading document relevance and checking context coverage...")
                result = ask_question(active_query, model=selected_model)
                elapsed = round(time.time() - start_time, 2)
                
                st.write("✍️ Synthesizing grounded answer with citations...")
                status_container.update(label=f"✅ Response completed in {elapsed}s", state="complete", expanded=False)

            answer = result.get("generation", "")
            citations = result.get("citations", [])

            st.markdown(answer)
            st.caption(f"⏱️ *Generated in {elapsed}s via `{selected_model}` & LangGraph.*")

            # Render Clean Professional Citations
            if citations:
                render_citations_ui(citations, expanded=True)

            # Save in history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "citations": citations,
                "latency": elapsed
            })

# -------------------------------------------------------------
# TAB 2: 12 CHAPTERS EXPLORER
# -------------------------------------------------------------
with tab_explorer:
    st.markdown("### 📖 All 12 Official Textbook Chapters (`preuniversity.grkraj.org`)")
    st.caption("Browse and read the complete source material used by the local RAG knowledge base.")
    
    chapter_files = sorted(list(CORPUS_DIR.glob("*.md")))
    if chapter_files:
        selected_ch = st.selectbox(
            "Select a chapter to read:",
            chapter_files,
            format_func=lambda x: x.stem.replace("Chapter_", "Chapter ").replace("_", " ")
        )
        if selected_ch:
            col_t, col_l = st.columns([3, 1])
            with col_t:
                st.markdown(f"#### 📖 {selected_ch.stem.replace('Chapter_', 'Chapter ').replace('_', ' ')}")
            with col_l:
                st.markdown(
                    f'<a class="sidebar-chapter-link" href="https://grkraj.org/pre-university/" target="_blank" rel="noopener noreferrer" style="justify-content:center; gap:8px;">'
                    f'<span>🌐 Open on Website</span><span>↗</span></a>',
                    unsafe_allow_html=True
                )
            ch_content = selected_ch.read_text(encoding="utf-8")
            with st.container(border=True):
                st.markdown(ch_content)
    else:
        st.warning("No chapters found in corpus directory. Click 'Sync Docs' in sidebar.")

# -------------------------------------------------------------
# TAB 3: SEARCH & RETRIEVAL INSPECTOR
# -------------------------------------------------------------
with tab_retriever_debug:
    st.markdown("### 🔍 Hybrid Retrieval Inspector")
    st.caption("Test how the search engine retrieves, ranks, and fuses dense and sparse results.")
    
    test_query = st.text_input("Enter a query to inspect retrieval ranks:", "What is the Casparian strip in root endodermis?")
    if st.button("Run Inspection", key="run_debug_retrieval"):
        try:
            retriever = HybridRetriever()
            dense_results = retriever.dense_search(test_query, k=3)
            sparse_results = retriever.sparse_search(test_query, k=3)
            hybrid_results = retriever.hybrid_retrieve(test_query, k_final=4)
            
            col_d, col_s = st.columns(2)
            with col_d:
                st.markdown("#### 🎯 Dense Vector Matches (ChromaDB)")
                for idx, (doc, score) in enumerate(dense_results):
                    with st.expander(f"Dense #{idx+1}: {doc.metadata.get('source')} (Score: {round(score, 3)})"):
                        st.markdown(f"**Section:** `{doc.metadata.get('section_title')}`")
                        st.caption(doc.page_content[:300] + "...")
                        
            with col_s:
                st.markdown("#### 🔤 Sparse Keyword Matches (BM25)")
                for idx, (doc, score) in enumerate(sparse_results):
                    with st.expander(f"BM25 #{idx+1}: {doc.metadata.get('source')} (Score: {round(score, 3)})"):
                        st.markdown(f"**Section:** `{doc.metadata.get('section_title')}`")
                        st.caption(doc.page_content[:300] + "...")
                        
            st.divider()
            st.markdown("#### ⚡ Fused Hybrid Ranking (Reciprocal Rank Fusion)")
            for idx, doc in enumerate(hybrid_results):
                st.success(f"**Rank #{idx+1} (Fusion Score: {doc.metadata.get('fusion_score')}):** {doc.metadata.get('source')} → *{doc.metadata.get('section_title')}*")
        except Exception as e:
            st.error(f"Error inspecting retrieval: {e}")
