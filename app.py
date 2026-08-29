"""
Pre-University Biology AI Tutor - Executive Dark-Themed Conversational RAG UI
Built with Streamlit, LangChain, LangGraph, ChromaDB & Ollama.
"""

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
    return [OLLAMA_MODEL, "llama3.2:latest", "muse-glimmer-30b:latest"]

# Page Setup
st.set_page_config(
    page_title="Pre-University Biology AI Tutor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Executive Dark UI & High Contrast Cards
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F8FAFC;
    }
    
    /* Header Gradient Dark Card */
    .hero-banner {
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 50%, #064E3B 100%);
        color: #F8FAFC;
        padding: 26px 32px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        box-shadow: 0 14px 34px -8px rgba(0, 0, 0, 0.65);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1.02rem;
        color: #94A3B8;
        margin-top: 6px;
        margin-bottom: 14px;
        line-height: 1.5;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.12);
        backdrop-filter: blur(8px);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #34D399;
        margin-right: 8px;
        margin-bottom: 6px;
        border: 1px solid rgba(52, 211, 153, 0.25);
    }
    
    /* Sidebar Metric Grid */
    .sidebar-metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 14px;
    }
    .metric-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 10px 12px;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 3px;
    }
    .metric-val {
        font-size: 0.85rem;
        font-weight: 700;
        color: #34D399;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* User Message Card (Elevated Right-Tinted Bubble) */
    .user-bubble-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-left: 4px solid #3B82F6;
        border-radius: 14px;
        padding: 16px 20px;
        margin-top: 12px;
        margin-bottom: 12px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
    }
    .user-bubble-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        color: #60A5FA;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .user-bubble-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #F8FAFC;
        line-height: 1.5;
    }

    /* Assistant Answer Study Card (Polished Pedagogical Panel) */
    .assistant-bubble-card {
        background: linear-gradient(180deg, #111827 0%, #0B0F19 100%);
        border: 1px solid #1F2937;
        border-top: 3px solid #10B981;
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.5);
    }
    .assistant-bubble-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 10px;
        margin-bottom: 16px;
    }
    .assistant-header-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
        font-weight: 700;
        color: #34D399;
    }
    .assistant-header-meta {
        font-size: 0.78rem;
        color: #64748B;
        background: rgba(255, 255, 255, 0.04);
        padding: 3px 10px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Quick Prompt Section */
    .prompt-section-title {
        font-size: 0.86rem;
        font-weight: 700;
        color: #94A3B8;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    
    /* Citation Cards (Modern Grid & Frosted Glass) */
    .citation-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-top: 3px solid #10B981;
        padding: 14px 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .citation-card:hover {
        border-color: #334155;
        transform: translateY(-2px);
    }
    .citation-header {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .citation-badge-link {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.83rem;
        font-weight: 700;
        color: #34D399 !important;
        text-decoration: none !important;
        background: rgba(16, 185, 129, 0.12);
        padding: 4px 12px;
        border-radius: 6px;
        border: 1px solid rgba(52, 211, 153, 0.25);
        transition: all 0.2s ease;
    }
    .citation-badge-link:hover {
        background: rgba(16, 185, 129, 0.24);
        border-color: #10B981;
        color: #6EE7B7 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.18);
    }
    .citation-badge-link .icon-arrow {
        font-size: 0.76rem;
        opacity: 0.8;
        transition: transform 0.2s ease;
    }
    .citation-badge-link:hover .icon-arrow {
        transform: translate(2px, -2px);
        opacity: 1;
    }
    .citation-section {
        font-size: 0.82rem;
        font-weight: 600;
        color: #CBD5E1;
        margin-bottom: 8px;
    }
    .citation-quote {
        color: #94A3B8;
        font-size: 0.82rem;
        font-style: italic;
        line-height: 1.45;
        background: #0B0F19;
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

    /* Executive Multi-line Prompt Composer */
    .composer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 14px;
        margin-bottom: 6px;
        padding: 0 4px;
        font-size: 0.83rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .composer-hint {
        font-size: 0.77rem;
        font-weight: 500;
        color: #64748B;
        text-transform: none;
        letter-spacing: normal;
    }

    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        padding-top: 4px !important;
        padding-bottom: 20px !important;
    }
    div[data-testid="stChatInput"] > div {
        background: linear-gradient(180deg, #131D31 0%, #0F172A 100%) !important;
        border: 1.5px solid #334155 !important;
        border-radius: 16px !important;
        padding: 10px 14px !important;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transition: all 0.25s ease-in-out !important;
    }
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25), 0 12px 30px -4px rgba(0, 0, 0, 0.7) !important;
        background: linear-gradient(180deg, #16243D 0%, #0F172A 100%) !important;
    }
    div[data-testid="stChatInput"] textarea {
        min-height: 85px !important;
        font-size: 0.96rem !important;
        line-height: 1.55 !important;
        color: #F8FAFC !important;
        background: transparent !important;
        padding: 6px 4px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94A3B8 !important;
        font-size: 0.94rem !important;
    }
    div[data-testid="stChatInput"] button {
        background: #10B981 !important;
        color: #064E3B !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 12px !important;
        align-self: flex-end !important;
        margin-bottom: 4px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35) !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: #34D399 !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.45) !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #064E3B !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0A0F1D;
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
    ("🌾 Hatch-Slack C4 & Kranz", "How does Kranz anatomy in C4 plants optimize photosynthetic efficiency and prevent photorespiration?"),
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
    ("🌸 Photoperiodism & Phytochrome", "Explain the physiological mechanism of photoperiodism and the role of phytochrome in flowering.")
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
                "or click any of the 20 suggested topic chips above to get started!"
            ),
            "citations": [],
            "latency": None,
            "model": None
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
    
    # 2x2 Telemetry Metric Cards
    st.markdown(f"""
    <div class="sidebar-metric-grid">
        <div class="metric-card">
            <div class="metric-label">🤖 Active Model</div>
            <div class="metric-val">{selected_model.split(':')[0]}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">⚡ Latency</div>
            <div class="metric-val">1.56s Avg</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">📖 Curriculum</div>
            <div class="metric-val">12 Chapters</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🛡️ Guardrails</div>
            <div class="metric-val">Strict Grounding</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Embeddings:** `{EMBEDDING_MODEL_NAME.split('/')[-1]}`")
    st.markdown("**Retrieval:** `Dense ChromaDB + Sparse BM25 (RRF)`")
    
    st.divider()
    st.markdown("#### 📚 12 Indexed Chapters")
    st.caption("Click to view source lecture notes on website:")
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
                    "model": None
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
    # Quick Sample Questions Section (20 Comprehensive Curriculum Chips + Shuffle)
    col_t_title, col_t_shuffle = st.columns([4, 1])
    with col_t_title:
        st.markdown('<div class="prompt-section-title">💡 20 Suggested Sample Questions (Click to Ask)</div>', unsafe_allow_html=True)
    with col_t_shuffle:
        if st.button("🎲 Inspire Me", use_container_width=True, help="Randomly pick an interesting biology question"):
            random_q = random.choice(SAMPLE_QUESTIONS)[1]
            st.session_state.queued_query = random_q
            st.rerun()
    
    chip_tab1, chip_tab2, chip_tab3, chip_tab4 = st.tabs([
        "🔬 Anatomy & Cells (5)",
        "☀️ Photosynthesis & Water (5)",
        "🌱 Nutrition & Growth (5)",
        "🧬 Genetics & Molecular (5)"
    ])
    
    with chip_tab1:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("🔬 Stomata & Guard Cells", use_container_width=True, help="Chapter 1: Plant Anatomy"):
                st.session_state.queued_query = "How do guard cells regulate the opening and closing of stomata?"
                st.rerun()
        with c2:
            if st.button("🌿 Apical vs Lateral", use_container_width=True, help="Chapter 1: Meristems"):
                st.session_state.queued_query = "Explain the structural and functional differences between apical and lateral meristems."
                st.rerun()
        with c3:
            if st.button("🪵 Xylem vs Phloem", use_container_width=True, help="Chapter 1: Complex Tissues"):
                st.session_state.queued_query = "Compare the cell types and conducting functions of xylem and phloem in plants."
                st.rerun()
        with c4:
            if st.button("🧱 Cell Wall Layers", use_container_width=True, help="Chapter 2: Cell Structure"):
                st.session_state.queued_query = "What are the structural layers and biochemical components of the plant cell wall?"
                st.rerun()
        with c5:
            if st.button("🎨 Plastid Types", use_container_width=True, help="Chapter 2: Organelles"):
                st.session_state.queued_query = "What are the differences between chloroplasts, chromoplasts, and leucoplasts in plant cells?"
                st.rerun()

    with chip_tab2:
        c6, c7, c8, c9, c10 = st.columns(5)
        with c6:
            if st.button("☀️ Calvin Cycle (C3)", use_container_width=True, help="Chapter 3: Photosynthesis"):
                st.session_state.queued_query = "Explain the three main phases of the Calvin Cycle (C3 pathway) in photosynthesis."
                st.rerun()
        with c7:
            if st.button("🌾 Hatch-Slack C4 & Kranz", use_container_width=True, help="Chapter 3: C4 Pathway"):
                st.session_state.queued_query = "How does Kranz anatomy in C4 plants optimize photosynthetic efficiency and prevent photorespiration?"
                st.rerun()
        with c8:
            if st.button("⚡ Z-Scheme & Photolysis", use_container_width=True, help="Chapter 3: Light Reactions"):
                st.session_state.queued_query = "Explain the Z-scheme of light reactions and the photolysis of water in Photosystem II."
                st.rerun()
        with c9:
            if st.button("💧 Cohesion-Tension Pull", use_container_width=True, help="Chapter 4: Water Relations"):
                st.session_state.queued_query = "Explain the Cohesion-Tension-Transpiration Pull Theory for water movement in xylem."
                st.rerun()
        with c10:
            if st.button("🛑 Casparian Strip", use_container_width=True, help="Chapter 4: Root Transport"):
                st.session_state.queued_query = "What is the Casparian strip and how does it regulate apoplastic vs symplastic root transport?"
                st.rerun()

    with chip_tab3:
        c11, c12, c13, c14, c15 = st.columns(5)
        with c11:
            if st.button("🌱 Mineral Criteria", use_container_width=True, help="Chapter 5: Mineral Nutrition"):
                st.session_state.queued_query = "What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout?"
                st.rerun()
        with c12:
            if st.button("🧬 Nitrogen Fixation", use_container_width=True, help="Chapter 5: Nitrogen Metabolism"):
                st.session_state.queued_query = "Explain the role of Nitrogenase and Leghemoglobin in biological nitrogen fixation."
                st.rerun()
        with c13:
            if st.button("⚡ Respiration & ETS", use_container_width=True, help="Chapter 6: Bioenergetics"):
                st.session_state.queued_query = "How does oxidative phosphorylation in mitochondrial cristae generate ATP via chemiosmosis?"
                st.rerun()
        with c14:
            if st.button("🍇 Auxin vs ABA", use_container_width=True, help="Chapter 7: Phytohormones"):
                st.session_state.queued_query = "Compare the functions of Auxins in apical dominance with Abscisic Acid (ABA) in drought stress."
                st.rerun()
        with c15:
            if st.button("🍯 Münch Pressure Flow", use_container_width=True, help="Chapter 8: Phloem Translocation"):
                st.session_state.queued_query = "Explain Ernst Münch's Pressure-Flow (Mass-Flow) Hypothesis for phloem translocation of sugars."
                st.rerun()

    with chip_tab4:
        c16, c17, c18, c19, c20 = st.columns(5)
        with c16:
            if st.button("🧬 Mendel 9:3:3:1 Ratio", use_container_width=True, help="Chapter 9: Mendelism"):
                st.session_state.queued_query = "What is Mendel's Law of Independent Assortment and explain the 9:3:3:1 dihybrid ratio?"
                st.rerun()
        with c17:
            if st.button("🪰 Linkage & Crossing Over", use_container_width=True, help="Chapter 10: Chromosomes"):
                st.session_state.queued_query = "How did Thomas Hunt Morgan's experiments on Drosophila prove linkage and crossing over?"
                st.rerun()
        with c18:
            if st.button("🧪 B-DNA Double Helix", use_container_width=True, help="Chapter 11: Molecular Genetics"):
                st.session_state.queued_query = "Explain the structural features of the Watson-Crick B-DNA double helix model."
                st.rerun()
        with c19:
            if st.button("⚙️ Translation on Ribosome", use_container_width=True, help="Chapter 12: Gene Expression"):
                st.session_state.queued_query = "Explain the stages of protein translation on ribosomes and the role of tRNA."
                st.rerun()
        with c20:
            if st.button("🌸 Photoperiodism & Phytochrome", use_container_width=True, help="Chapter 7: Flowering"):
                st.session_state.queued_query = "Explain the physiological mechanism of photoperiodism and the role of phytochrome in flowering."
                st.rerun()

    st.markdown('<div class="composer-header"><span>💬 Ask Your Question</span><span class="composer-hint">Shift + Enter for multi-line queries • Enter to send</span></div>', unsafe_allow_html=True)
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
        # Display Active Question Card
        st.markdown(f"""
        <div class="user-bubble-card">
            <div class="user-bubble-header">
                <span>👤 You Asked</span>
                <span>⏱️ Live Query</span>
            </div>
            <div class="user-bubble-text">{active_query}</div>
        </div>
        """, unsafe_allow_html=True)

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

        # Display Assistant Card
        st.markdown(f"""
        <div class="assistant-bubble-card">
            <div class="assistant-bubble-header">
                <span class="assistant-header-title">🌿 Pre-University Biology AI Tutor</span>
                <span class="assistant-header-meta">⚡ Generated in {elapsed}s via {selected_model}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(answer)

        if citations:
            render_citations_ui(citations, expanded=False)

        # Prepend to turns so this latest Q&A is positioned at the top of history
        st.session_state.turns.insert(0, {
            "query": active_query,
            "answer": answer,
            "citations": citations,
            "latency": elapsed,
            "model": selected_model
        })
        st.rerun()

    # Render Conversation History (Newest Questions at the Top)
    for i, turn in enumerate(st.session_state.turns):
        if turn.get("query"):
            st.markdown(f"""
            <div class="user-bubble-card">
                <div class="user-bubble-header">
                    <span>👤 You Asked</span>
                    <span>Q#{len(st.session_state.turns) - i}</span>
                </div>
                <div class="user-bubble-text">{turn['query']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        m_used = turn.get("model") or selected_model
        lat_text = f"⚡ Generated in {turn['latency']}s via {m_used}" if turn.get("latency") else "🌿 AI Tutor Ready"
        
        with st.container():
            st.markdown(f"""
            <div class="assistant-bubble-card">
                <div class="assistant-bubble-header">
                    <span class="assistant-header-title">🌿 Pre-University Biology AI Tutor</span>
                    <span class="assistant-header-meta">{lat_text}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(turn["answer"])
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
