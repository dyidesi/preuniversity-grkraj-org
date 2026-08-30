"""
Pre-University Biology AI Tutor - Refined Professional Conversational RAG UI
Built with Streamlit, LangChain, LangGraph, ChromaDB & Ollama.
Supports Multi-Provider LLMs: Demo/Mock Mode (Zero Setup), Local Ollama, Google Gemini, OpenAI, Anthropic, and Groq.
"""

import os
import importlib
import streamlit as st
import time
import json
import random
from pathlib import Path
import requests

import src.config
importlib.reload(src.config)
import src.agent_graph
importlib.reload(src.agent_graph)

from src.config import CORPUS_DIR, OLLAMA_MODEL, EMBEDDING_MODEL_NAME, OLLAMA_BASE_URL
try:
    from src.config import get_chapter_url
except ImportError:
    def get_chapter_url(source_name: str) -> str:
        return "https://grkraj.org/pre-university"

from src.agent_graph import (
    ask_question,
    reset_retriever,
    list_local_ollama_models,
    is_ollama_alive
)
from src.ingestion import run_ingestion
from src.hybrid_retriever import HybridRetriever

# Page Setup
st.set_page_config(
    page_title="Pre-University Biology AI Tutor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Tasteful, Professional Dark UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #E2E8F0;
    }
    
    /* Global Typography Restraints */
    .stMarkdown h1, h1 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
        margin-top: 14px !important;
        margin-bottom: 8px !important;
        line-height: 1.4 !important;
        border-bottom: 1px solid #1E293B !important;
        padding-bottom: 4px !important;
    }
    .stMarkdown h2, h2 {
        font-size: 1.12rem !important;
        font-weight: 600 !important;
        color: #F1F5F9 !important;
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        line-height: 1.35 !important;
    }
    .stMarkdown h3, h3 {
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        color: #E2E8F0 !important;
        margin-top: 10px !important;
        margin-bottom: 4px !important;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
        color: #CBD5E1 !important;
    }
    .stMarkdown ul, .stMarkdown ol {
        margin-top: 6px !important;
        margin-bottom: 10px !important;
        padding-left: 20px !important;
    }
    .stMarkdown li {
        margin-bottom: 4px !important;
    }
    
    /* Clean, Understated Header Card */
    .hero-banner {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-left: 4px solid #10B981;
        padding: 20px 24px;
        border-radius: 14px;
        margin-bottom: 18px;
    }
    .hero-title {
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
    }
    .hero-subtitle {
        font-size: 0.92rem;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        background: #1E293B;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
        color: #94A3B8;
        margin-right: 6px;
        margin-bottom: 4px;
        border: 1px solid #334155;
    }
    .badge-pill.accent {
        color: #34D399;
        border-color: rgba(52, 211, 153, 0.3);
        background: rgba(16, 185, 129, 0.08);
    }
    
    /* Sidebar Metrics Grid */
    .sidebar-metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 14px;
    }
    .metric-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 8px 10px;
    }
    .metric-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .metric-val {
        font-size: 0.82rem;
        font-weight: 600;
        color: #34D399;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Section Subheading */
    .prompt-section-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #94A3B8;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Citation Cards (Clean, Understated) */
    .citation-card {
        background: #0B0F19;
        border: 1px solid #1E293B;
        border-top: 2px solid #10B981;
        padding: 12px 14px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .citation-header {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
    }
    .citation-badge-link {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #34D399 !important;
        text-decoration: none !important;
        background: rgba(16, 185, 129, 0.1);
        padding: 3px 10px;
        border-radius: 6px;
        border: 1px solid rgba(52, 211, 153, 0.2);
        transition: all 0.15s ease;
    }
    .citation-badge-link:hover {
        background: rgba(16, 185, 129, 0.2);
        border-color: #10B981;
        color: #6EE7B7 !important;
    }
    .citation-badge-link .icon-arrow {
        font-size: 0.72rem;
        opacity: 0.8;
    }
    .citation-section {
        font-size: 0.8rem;
        font-weight: 500;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .citation-quote {
        color: #94A3B8;
        font-size: 0.8rem;
        font-style: italic;
        line-height: 1.45;
        background: #070B13;
        padding: 8px 10px;
        border-radius: 6px;
        border-left: 2px solid #3B82F6;
    }
    
    /* Buttons in Dark Mode */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #334155;
        background-color: #1E293B;
        color: #E2E8F0;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 6px 12px;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        border-color: #10B981;
        color: #10B981;
        background-color: #0F172A;
    }
    
    /* Sidebar chapter links */
    .sidebar-chapter-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 10px;
        margin-bottom: 4px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 6px;
        color: #CBD5E1 !important;
        text-decoration: none !important;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.15s ease;
    }
    .sidebar-chapter-link:hover {
        background: rgba(16, 185, 129, 0.12);
        border-color: #10B981;
        color: #34D399 !important;
    }
    .sidebar-chapter-icon {
        font-size: 0.75rem;
        color: #64748B;
    }

    /* Executive Multi-line Prompt Composer */
    .composer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 6px;
        padding: 0 2px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .composer-hint {
        font-size: 0.74rem;
        font-weight: 400;
        color: #64748B;
        text-transform: none;
    }

    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        padding-top: 2px !important;
        padding-bottom: 16px !important;
    }
    div[data-testid="stChatInput"] > div {
        background: #0F172A !important;
        border: 1.5px solid #334155 !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        transition: border-color 0.2s ease !important;
    }
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2) !important;
    }
    div[data-testid="stChatInput"] textarea {
        min-height: 75px !important;
        font-size: 0.94rem !important;
        line-height: 1.5 !important;
        color: #F8FAFC !important;
        background: transparent !important;
        padding: 4px 2px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64748B !important;
        font-size: 0.9rem !important;
    }
    div[data-testid="stChatInput"] button {
        background: #10B981 !important;
        color: #064E3B !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 6px 10px !important;
        align-self: flex-end !important;
        margin-bottom: 2px !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: #34D399 !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #064E3B !important;
    }

    /* Native Chat Message Clean Layout */
    div[data-testid="stChatMessage"] {
        background: #0B0F19 !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #080D1A;
        border-right: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Sample Questions Repository (All 20 Curriculum Queries)
SAMPLE_QUESTIONS = [
    # Category 1: Anatomy & Cells
    ("🔬 Stomata & Guard Cells", "How do guard cells regulate the opening and closing of stomata?"),
    ("🌿 Apical vs Lateral", "Explain the structural and functional differences between apical and lateral meristems."),
    ("🪵 Xylem vs Phloem", "Compare the cell types and conducting functions of xylem and phloem in plants."),
    ("🧱 Cell Wall Layers", "What are the structural layers and biochemical components of the plant cell wall?"),
    ("🎨 Plastid Types", "What are the differences between chloroplasts, chromoplasts, and leucoplasts in plant cells?"),
    
    # Category 2: Photosynthesis & Water
    ("☀️ Calvin Cycle (C3)", "Explain the three main phases of the Calvin Cycle (C3 pathway) in photosynthesis."),
    ("🌾 Hatch-Slack C4", "How does Kranz anatomy in C4 plants optimize photosynthetic efficiency and prevent photorespiration?"),
    ("⚡ Z-Scheme & Photolysis", "Explain the Z-scheme of light reactions and the photolysis of water in Photosystem II."),
    ("💧 Cohesion-Tension Pull", "Explain the Cohesion-Tension-Transpiration Pull Theory for water movement in xylem."),
    ("🛑 Casparian Strip", "What is the Casparian strip and how does it regulate apoplastic vs symplastic root transport?"),
    
    # Category 3: Nutrition & Growth
    ("🌱 Mineral Criteria", "What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout?"),
    ("🧬 Nitrogen Fixation", "Explain the role of Nitrogenase and Leghemoglobin in biological nitrogen fixation."),
    ("⚡ Respiration & ETS", "How does oxidative phosphorylation in mitochondrial cristae generate ATP via chemiosmosis?"),
    ("🍇 Auxin vs ABA", "Compare the functions of Auxins in apical dominance with Abscisic Acid (ABA) in drought stress."),
    ("🍯 Münch Pressure Flow", "Explain Ernst Münch's Pressure-Flow (Mass-Flow) Hypothesis for phloem translocation of sugars."),
    
    # Category 4: Genetics & Molecular
    ("🧬 Mendel 9:3:3:1 Ratio", "What is Mendel's Law of Independent Assortment and explain the 9:3:3:1 dihybrid ratio?"),
    ("🪰 Linkage & Crossing Over", "How did Thomas Hunt Morgan's experiments on Drosophila prove linkage and crossing over?"),
    ("🧪 B-DNA Double Helix", "Explain the structural features of the Watson-Crick B-DNA double helix model."),
    ("⚙️ Translation on Ribosome", "Explain the stages of protein translation on ribosomes and the role of tRNA."),
    ("🌸 Photoperiodism", "Explain the physiological mechanism of photoperiodism and the role of phytochrome in flowering.")
]

# Initialize Session State
if "turns" not in st.session_state:
    st.session_state.turns = [
        {
            "query": None,
            "answer": (
                "👋 **Welcome! I am your Pre-University Biology AI Tutor.**\n\n"
                "I am strictly grounded in all **12 official textbook chapters** from **preuniversity.grkraj.org** "
                "(authored by Prof. Dr. G. R. Kantharaj). You can freely type any conceptual question in the chat bar below, "
                "or click any of the suggested topic chips above to get started!"
            ),
            "citations": [],
            "latency": None,
            "provider": "Mock Mode",
            "model": "Instant"
        }
    ]

if "queued_query" not in st.session_state:
    st.session_state.queued_query = None

# Sidebar Content
with st.sidebar:
    st.markdown("### 🌿 Biology Tutor Studio")
    st.caption("Local & Cloud Agentic RAG • LangChain & LangGraph")
    
    st.divider()
    st.markdown("#### ⚙️ Model Configuration")
    
    # 1. LLM Provider Selector (Matching user specification)
    provider_options = [
        "Ollama (Local)",
        "Demo / Mock Mode (Zero Setup)",
        "Google Gemini",
        "OpenAI",
        "Anthropic",
        "Groq (Cloud Llama)"
    ]
    
    # Default selection logic: if on cloud and no Ollama, default to Demo/Mock Mode
    default_provider_idx = 0 if is_ollama_alive() else 1
    selected_provider_label = st.selectbox(
        "LLM Provider",
        options=provider_options,
        index=default_provider_idx,
        help="Select which AI inference engine or mode to power your biology tutor"
    )
    
    # Provider-Specific Parameters
    selected_model_name = "llama3.2:latest"
    user_api_key = None
    custom_base_url = OLLAMA_BASE_URL
    provider_key = "ollama"
    
    if selected_provider_label == "Demo / Mock Mode (Zero Setup)":
        provider_key = "mock"
        selected_model_name = "Demo Knowledge Synthesizer"
        st.info("⚡ **Instant Mode Active**: Pre-synthesized authoritative walkthroughs from the 12 chapters. Zero API keys or credits required!")

    elif selected_provider_label == "Ollama (Local)":
        provider_key = "ollama"
        custom_base_url = st.text_input("Ollama Base URL:", value=OLLAMA_BASE_URL)
        local_models = list_local_ollama_models(base_url=custom_base_url)
        default_m_idx = local_models.index(OLLAMA_MODEL) if OLLAMA_MODEL in local_models else 0
        selected_model_name = st.selectbox("Ollama Model:", options=local_models, index=default_m_idx)
        if not is_ollama_alive(custom_base_url):
            st.warning("⚠️ Local Ollama is not detected at this URL. Make sure Ollama is running or switch to **Demo / Mock Mode**.")

    elif selected_provider_label == "Google Gemini":
        provider_key = "google"
        gemini_models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        selected_model_name = st.selectbox("Gemini Model:", options=gemini_models, index=0)
        default_gemini_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
        user_api_key = st.text_input("Gemini API Key:", value=default_gemini_key, type="password", help="Enter your Google AI Studio API key")

    elif selected_provider_label == "OpenAI":
        provider_key = "openai"
        openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
        selected_model_name = st.selectbox("OpenAI Model:", options=openai_models, index=0)
        default_openai_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
        user_api_key = st.text_input("OpenAI API Key:", value=default_openai_key, type="password", help="Enter your OpenAI API key")

    elif selected_provider_label == "Anthropic":
        provider_key = "anthropic"
        anthropic_models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]
        selected_model_name = st.selectbox("Claude Model:", options=anthropic_models, index=0)
        default_anthropic_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
        user_api_key = st.text_input("Anthropic API Key:", value=default_anthropic_key, type="password", help="Enter your Anthropic API key")

    elif selected_provider_label == "Groq (Cloud Llama)":
        provider_key = "groq"
        groq_models = ["llama-3.3-70b-versatile", "llama-3.2-3b-preview", "mixtral-8x7b-32768"]
        selected_model_name = st.selectbox("Groq Model:", options=groq_models, index=0)
        default_groq_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY", "")
        user_api_key = st.text_input("Groq API Key:", value=default_groq_key, type="password", help="Enter your Groq API key")

    # Clean Metric Grid
    st.markdown(f"""
    <div class="sidebar-metric-grid">
        <div class="metric-card">
            <div class="metric-label">Provider</div>
            <div class="metric-val">{selected_provider_label.split(' ')[0]}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Status</div>
            <div class="metric-val">Ready</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Curriculum</div>
            <div class="metric-val">12 Chapters</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Grounding</div>
            <div class="metric-val">Strict RAG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Embeddings: `{EMBEDDING_MODEL_NAME.split('/')[-1]}`")
    st.caption("Retrieval: `Dense ChromaDB + Sparse BM25 (RRF)`")
    
    st.divider()
    st.markdown("#### 📚 12 Indexed Chapters")
    st.caption("Direct lecture notes on website:")
    chapters = sorted(list(CORPUS_DIR.glob("*.md")))
    for ch in chapters:
        chapter_name = ch.stem.replace("Chapter_", "Ch. ").replace("_", " ")
        chapter_url = get_chapter_url(ch.name)
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
            st.session_state.turns = [
                {
                    "query": None,
                    "answer": "Conversation cleared. How can I assist you with your pre-university biology studies?",
                    "citations": [],
                    "latency": None,
                    "provider": selected_provider_label,
                    "model": selected_model_name
                }
            ]
            st.rerun()

    # Chat Export Option
    if len(st.session_state.turns) > 1 or (len(st.session_state.turns) == 1 and st.session_state.turns[0].get("query")):
        chat_export_json = json.dumps(st.session_state.turns, indent=2)
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
                raw_src = c.get("raw_source") or source_title
                url = c.get("url")
                if not url or url == "https://grkraj.org/pre-university/":
                    url = get_chapter_url(raw_src)
                
                card_html = f"""
                <div class="citation-card">
                    <div class="citation-header">
                        <a class="citation-badge-link" href="{url}" target="_blank" rel="noopener noreferrer" title="Click to view chapter lecture notes on grkraj.org">
                            <span>[{i+1}] {source_title}</span>
                            <span class="icon-arrow">↗</span>
                        </a>
                    </div>
                    <div class="citation-section">📌 <i>Section: {section_title}</i></div>
                    <div class="citation-quote">"{snippet}"</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

# Main Header Banner (Refined, Professional Dark Card)
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">
        <span>🌿 Pre-University Biology AI Tutor</span>
    </div>
    <div class="hero-subtitle">
        Local & Cloud conversational assistant grounded in all 12 curriculum chapters from <b>preuniversity.grkraj.org</b>
    </div>
    <div>
        <span class="badge-pill accent">⚡ LangGraph State Machine</span>
        <span class="badge-pill">🔍 Hybrid BM25 + Chroma</span>
        <span class="badge-pill">🛡️ Strict Factual Grounding</span>
        <span class="badge-pill">📖 12 Chapters</span>
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
    col_t_title, col_t_shuffle = st.columns([4, 1])
    with col_t_title:
        st.markdown('<div class="prompt-section-title">Suggested Study Topics (Click to ask)</div>', unsafe_allow_html=True)
    with col_t_shuffle:
        if st.button("🎲 Inspire Me", use_container_width=True, help="Randomly select an interesting biology question"):
            random_q = random.choice(SAMPLE_QUESTIONS)[1]
            st.session_state.queued_query = random_q
            st.rerun()
    
    chip_tab1, chip_tab2, chip_tab3, chip_tab4 = st.tabs([
        "Anatomy & Cells (5)",
        "Photosynthesis & Water (5)",
        "Nutrition & Growth (5)",
        "Genetics & Molecular (5)"
    ])
    
    with chip_tab1:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("🔬 Stomata & Guard Cells", use_container_width=True):
                st.session_state.queued_query = "How do guard cells regulate the opening and closing of stomata?"
                st.rerun()
        with c2:
            if st.button("🌿 Apical vs Lateral", use_container_width=True):
                st.session_state.queued_query = "Explain the structural and functional differences between apical and lateral meristems."
                st.rerun()
        with c3:
            if st.button("🪵 Xylem vs Phloem", use_container_width=True):
                st.session_state.queued_query = "Compare the cell types and conducting functions of xylem and phloem in plants."
                st.rerun()
        with c4:
            if st.button("🧱 Cell Wall Layers", use_container_width=True):
                st.session_state.queued_query = "What are the structural layers and biochemical components of the plant cell wall?"
                st.rerun()
        with c5:
            if st.button("🎨 Plastid Types", use_container_width=True):
                st.session_state.queued_query = "What are the differences between chloroplasts, chromoplasts, and leucoplasts in plant cells?"
                st.rerun()

    with chip_tab2:
        c6, c7, c8, c9, c10 = st.columns(5)
        with c6:
            if st.button("☀️ Calvin Cycle (C3)", use_container_width=True):
                st.session_state.queued_query = "Explain the three main phases of the Calvin Cycle (C3 pathway) in photosynthesis."
                st.rerun()
        with c7:
            if st.button("🌾 Hatch-Slack C4", use_container_width=True):
                st.session_state.queued_query = "How does Kranz anatomy in C4 plants optimize photosynthetic efficiency and prevent photorespiration?"
                st.rerun()
        with c8:
            if st.button("⚡ Z-Scheme & Photolysis", use_container_width=True):
                st.session_state.queued_query = "Explain the Z-scheme of light reactions and the photolysis of water in Photosystem II."
                st.rerun()
        with c9:
            if st.button("💧 Cohesion-Tension Pull", use_container_width=True):
                st.session_state.queued_query = "Explain the Cohesion-Tension-Transpiration Pull Theory for water movement in xylem."
                st.rerun()
        with c10:
            if st.button("🛑 Casparian Strip", use_container_width=True):
                st.session_state.queued_query = "What is the Casparian strip and how does it regulate apoplastic vs symplastic root transport?"
                st.rerun()

    with chip_tab3:
        c11, c12, c13, c14, c15 = st.columns(5)
        with c11:
            if st.button("🌱 Mineral Criteria", use_container_width=True):
                st.session_state.queued_query = "What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout?"
                st.rerun()
        with c12:
            if st.button("🧬 Nitrogen Fixation", use_container_width=True):
                st.session_state.queued_query = "Explain the role of Nitrogenase and Leghemoglobin in biological nitrogen fixation."
                st.rerun()
        with c13:
            if st.button("⚡ Respiration & ETS", use_container_width=True):
                st.session_state.queued_query = "How does oxidative phosphorylation in mitochondrial cristae generate ATP via chemiosmosis?"
                st.rerun()
        with c14:
            if st.button("🍇 Auxin vs ABA", use_container_width=True):
                st.session_state.queued_query = "Compare the functions of Auxins in apical dominance with Abscisic Acid (ABA) in drought stress."
                st.rerun()
        with c15:
            if st.button("🍯 Münch Pressure Flow", use_container_width=True):
                st.session_state.queued_query = "Explain Ernst Münch's Pressure-Flow (Mass-Flow) Hypothesis for phloem translocation of sugars."
                st.rerun()

    with chip_tab4:
        c16, c17, c18, c19, c20 = st.columns(5)
        with c16:
            if st.button("🧬 Mendel 9:3:3:1 Ratio", use_container_width=True):
                st.session_state.queued_query = "What is Mendel's Law of Independent Assortment and explain the 9:3:3:1 dihybrid ratio?"
                st.rerun()
        with c17:
            if st.button("🪰 Linkage & Crossing Over", use_container_width=True):
                st.session_state.queued_query = "How did Thomas Hunt Morgan's experiments on Drosophila prove linkage and crossing over?"
                st.rerun()
        with c18:
            if st.button("🧪 B-DNA Double Helix", use_container_width=True):
                st.session_state.queued_query = "Explain the structural features of the Watson-Crick B-DNA double helix model."
                st.rerun()
        with c19:
            if st.button("⚙️ Translation on Ribosome", use_container_width=True):
                st.session_state.queued_query = "Explain the stages of protein translation on ribosomes and the role of tRNA."
                st.rerun()
        with c20:
            if st.button("🌸 Photoperiodism", use_container_width=True):
                st.session_state.queued_query = "Explain the physiological mechanism of photoperiodism and the role of phytochrome in flowering."
                st.rerun()

    st.markdown('<div class="composer-header"><span>Ask Your Question</span><span class="composer-hint">Shift + Enter for new lines • Enter to submit</span></div>', unsafe_allow_html=True)
    user_typed_input = st.chat_input("Type any biology question here (e.g., 'What is the role of the Casparian strip?')...")

    # Determine query to process (either typed by user or clicked from quick prompts)
    active_query = None
    if user_typed_input:
        active_query = user_typed_input
    elif st.session_state.queued_query:
        active_query = st.session_state.queued_query
        st.session_state.queued_query = None

    # Execute RAG Pipeline on Active Query (Runs immediately at the top)
    if active_query:
        # Display Active Question
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**{active_query}**")

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🌿"):
            status_container = st.status(f"Analyzing textbook chapters via {selected_provider_label}...", expanded=True)
            
            with status_container:
                st.write("🔍 Running Hybrid Retrieval (Dense Chroma + Sparse BM25)...")
                start_time = time.time()
                
                st.write("⚖️ Grading document relevance and checking context coverage...")
                result = ask_question(
                    active_query,
                    provider=provider_key,
                    model=selected_model_name,
                    api_key=user_api_key,
                    base_url=custom_base_url
                )
                elapsed = round(time.time() - start_time, 2)
                
                st.write("✍️ Synthesizing grounded explanation with citations...")
                status_container.update(label=f"✅ Completed in {elapsed}s", state="complete", expanded=False)

            answer = result.get("generation", "")
            citations = result.get("citations", [])

            st.markdown(answer)
            st.caption(f"⏱️ Generated in {elapsed}s via `{selected_provider_label} ({selected_model_name.split(':')[0]})` • LangGraph")

            if citations:
                render_citations_ui(citations, expanded=False)

        # Prepend to turns so this latest Q&A is positioned at the top of history
        st.session_state.turns.insert(0, {
            "query": active_query,
            "answer": answer,
            "citations": citations,
            "latency": elapsed,
            "provider": selected_provider_label,
            "model": selected_model_name
        })
        st.rerun()

    # Render Conversation History (Newest Questions at the Top)
    for turn in st.session_state.turns:
        if turn.get("query"):
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**{turn['query']}**")
                
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(turn["answer"])
            if turn.get("latency"):
                prov_tag = turn.get("provider") or selected_provider_label
                mod_tag = turn.get("model") or selected_model_name
                st.caption(f"⏱️ Generated in {turn['latency']}s via `{prov_tag} ({mod_tag.split(':')[0]})` • LangGraph")
            if turn.get("citations"):
                render_citations_ui(turn["citations"], expanded=False)

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
            ch_url = get_chapter_url(selected_ch.name)
            col_t, col_l = st.columns([3, 1])
            with col_t:
                st.markdown(f"#### 📖 {selected_ch.stem.replace('Chapter_', 'Chapter ').replace('_', ' ')}")
            with col_l:
                st.markdown(
                    f'<a class="sidebar-chapter-link" href="{ch_url}" target="_blank" rel="noopener noreferrer" style="justify-content:center; gap:8px;">'
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
    st.markdown("### 🔍 Hybrid Retrieval Inspector (Dense Chroma + Sparse BM25)")
    st.caption("Inspect document chunk rankings, similarity metrics, and Reciprocal Rank Fusion (RRF) scores.")
    
    debug_query = st.text_input("Test Retrieval Query:", value="Calvin cycle carbon fixation RuBisCO enzyme")
    if debug_query:
        retriever = HybridRetriever()
        dense_hits = retriever.dense_search(debug_query, k=4)
        sparse_hits = retriever.sparse_search(debug_query, k=4)
        hybrid_hits = retriever.hybrid_retrieve(debug_query, k_final=4)

        col_d, col_s = st.columns(2)
        with col_d:
            st.markdown("#### 🧠 Dense ChromaDB Semantic Hits")
            for rank, (d, score) in enumerate(dense_hits):
                st.markdown(f"**Rank {rank+1}** • *Distance: {score:.4f}* • `{d.metadata.get('source')}`")
                st.caption(f"📌 {d.metadata.get('section_title')}")
                st.info(d.page_content[:250] + "...")

        with col_s:
            st.markdown("#### ⚡ Sparse BM25 Keyword Hits")
            for rank, (d, score) in enumerate(sparse_hits):
                st.markdown(f"**Rank {rank+1}** • *BM25 Score: {score:.4f}* • `{d.metadata.get('source')}`")
                st.caption(f"📌 {d.metadata.get('section_title')}")
                st.info(d.page_content[:250] + "...")

        st.markdown("---")
        st.markdown("#### 🏆 Final Hybrid Fused Ranks (Reciprocal Rank Fusion)")
        for rank, d in enumerate(hybrid_hits):
            f_score = d.metadata.get('fusion_score', 0)
            st.success(f"**Rank {rank+1}** • *RRF Fusion Score: {f_score:.5f}* • **{d.metadata.get('source')}** (`{d.metadata.get('section_title')}`)\n\n{d.page_content}")
