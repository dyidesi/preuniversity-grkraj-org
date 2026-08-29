# 🌿 Pre-University Biology AI Tutor (Local Agentic RAG)

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-10B981?style=for-the-badge&logo=github)](https://github.com/dyidesi/preuniversity-grkraj-org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-orange?style=for-the-badge)](https://langchain.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_RAG-purple?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge&logo=ollama)](https://ollama.ai)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dark_Theme-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)

A 100% local, stateful, agentic Retrieval-Augmented Generation (RAG) study assistant built over all **12 official Pre-University Biology chapters** from [preuniversity.grkraj.org](https://grkraj.org/pre-university/) (authored by **Prof. Dr. G. R. Kantharaj**, Bangalore University).

---

## 🎯 Key Features & Innovations

1. **Full 12-Chapter Knowledge Base**:
   - Covers the entire Pre-University curriculum: *Plant Anatomy, Cell Structure, Photosynthesis, Water Relations, Mineral Nutrition, Respiration, Phytohormones, Phloem Translocation, Mendelism, Linkage, DNA Structure, and Gene Expression*.
   - Clickable sidebar chapter links opening directly to live lecture notes on `https://grkraj.org/pre-university/` in new browser tabs.

2. **Dynamic Local Model Selector**:
   - Choose between **Muse Glimmer (`muse-glimmer-30b:latest`)**, **Llama 3.2 (`llama3.2:latest`)**, **Gemma 4 (`gemma4:e4b-it-q8_0`)**, or any locally installed Ollama model directly via the sidebar dropdown.

3. **Hybrid Dense + Sparse Retrieval with Reciprocal Rank Fusion (RRF)**:
   - Dense semantic vector search via **ChromaDB** (`sentence-transformers/all-MiniLM-L6-v2`).
   - Sparse exact keyword search via **BM25Okapi** (`rank-bm25`).
   - Combined using **Reciprocal Rank Fusion (RRF)** to capture both conceptual semantics and exact biological terms.

4. **Corrective Agentic LangGraph Workflow**:
   - **Document Relevance Grading**: Binary relevancy verification of retrieved context.
   - **Query Transformation**: Rephrases search queries if initial retrieval is low-confidence.
   - **Grounded Generation with Inline Citations**: Formats answers with explicit `[Chapter X: Section Y]` citations.
   - **Anti-Hallucination Guardrail & Safe Refusal**: Deterministically triggers an "I don't know" fallback when questions fall outside the curriculum.

5. **Modern Dark-Themed Dashboard UI**:
   - **Dual Input**: Seamlessly type custom questions in the bottom chat bar or click quick suggested topic chips across the curriculum.
   - **Professional 2-Column Citation Grid**: Frosted glass cards with chapter badges, section indicators, clean quote bubbles (raw markdown stripped), and direct website buttons.
   - **In-App Reader Tab**: Read any of the 12 textbook chapters directly inside the application with math formula rendering.
   - **Retrieval Inspector Tab**: Interactive debugger displaying raw ChromaDB dense matches, BM25 scores, and fused hybrid rankings.

6. **15-Question Benchmark Suite**:
   - Pre-configured evaluation suite scoring factual accuracy, multi-hop reasoning, and out-of-domain refusal handling.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    User([Student / User]) -->|Ask Question / Select Model| UI[Streamlit Dark Chat UI (app.py)]
    UI --> Graph[LangGraph Agentic Graph (src/agent_graph.py)]
    
    subgraph Knowledge Storage
        Corpus[12 Chapter Markdown Files] --> Ingest[Ingestion Pipeline (src/ingestion.py)]
        Ingest --> Chroma[(ChromaDB Vector Store)]
        Ingest --> BM25[(BM25 Sparse Index)]
        Chroma --> Hybrid[Hybrid Retriever (src/hybrid_retriever.py)]
        BM25 --> Hybrid
    end

    subgraph LangGraph Pipeline
        Graph --> NodeRetrieve[1. Hybrid Search: BM25 + Dense Chroma]
        NodeRetrieve --> NodeGrade[2. Grade Document Relevance]
        NodeGrade -->|Relevant| NodeGenerate[3. Grounded Generator with Selected Model]
        NodeGrade -->|Irrelevant| NodeRewrite[Query Rewriter & Retry]
        NodeRewrite --> NodeRetrieve
        NodeGenerate --> NodeHallucination[4. Grounding Check]
        NodeHallucination -->|Grounded| UIOutput[Render Answer + 2-Col Citation Grid]
        NodeHallucination -->|Ungrounded / No Docs| Refusal[Deterministic Safe Refusal]
    end
    
    Refusal --> UIOutput
```

---

## 📚 Indexed 12 Chapters Overview

| # | Chapter Title | Topic Scope & Key Concepts |
| :-: | :--- | :--- |
| **01** | **Plant Anatomy & Tissue Systems** | Meristems, Parenchyma, Collenchyma, Sclerenchyma, Xylem & Phloem, Stomatal guard cell turgor |
| **02** | **Plant Cell Structure & Organelles** | Cell Wall, Middle Lamella, Plasmodesmata, Plastids (Chloroplasts, Chromoplasts, Leucoplasts), Mitochondria, Central Vacuole |
| **03** | **Photosynthesis in Higher Plants** | Z-Scheme photolysis, PSI/PSII, Calvin Cycle (C3), Hatch-Slack (C4), Kranz Anatomy, RuBisCO vs PEP Carboxylase |
| **04** | **Plant-Water Relations & Transpiration** | Water potential ($\Psi_w = \Psi_s + \Psi_p$), Osmosis, Apoplast vs Symplast, Casparian Strip, Dixon-Joly Cohesion-Tension Theory |
| **05** | **Mineral Nutrition in Plants** | Arnon-Stout criteria, Macro/Micro nutrients, Nitrogen Cycle, Biological Nitrogen Fixation, Nitrogenase & Leghemoglobin |
| **06** | **Respiration in Plants & Bioenergetics** | Glycolysis (EMP Pathway), Krebs/TCA Cycle, Mitochondrial Cristae Electron Transport Chain, Chemiosmosis & ATP Synthase |
| **07** | **Plant Growth Regulators & Phytohormones** | Auxins (apical dominance), Gibberellins (bolting/dormancy), Cytokinins (cell division), ABA (drought stress/stomatal closure), Ethylene |
| **08** | **Translocation of Organic Solutes** | Source-Sink dynamics, Sieve Tubes & Companion Cells, Ernst Münch Mass-Flow / Pressure-Flow Hypothesis |
| **09** | **Principles of Genetics & Mendelism** | Mendel's 7 contrasting traits in *Pisum sativum*, Monohybrid (3:1 / 1:2:1), Dihybrid (9:3:3:1), Laws of Segregation & Independent Assortment |
| **10** | **Chromosomal Basis of Inheritance & Linkage** | Sutton-Boveri Chromosomal Theory, T.H. Morgan's *Drosophila* X-linkage, Crossing Over, Genetic Mapping (cM), Chromosomal aberrations |
| **11** | **Molecular Basis of Inheritance & DNA Structure** | Griffith, Avery-MacLeod-McCarty, Hershey-Chase experiments, Watson-Crick B-DNA Double Helix, Meselson-Stahl Semiconservative Replication |
| **12** | **Gene Expression, Transcription & Translation** | Central Dogma, RNA Polymerase transcription, 5' Capping / Splicing, Genetic Code (AUG start codon), Ribosomal translation stages |

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/dyidesi/preuniversity-grkraj-org.git
cd preuniversity-grkraj-org

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Ensure Ollama is Running with Models
Make sure Ollama is installed and running:
```bash
ollama run muse-glimmer-30b:latest
# Or pull other lightweight models:
ollama pull llama3.2
```

### 3. Ingest & Index the Knowledge Base
```bash
python -m src.ingestion
```
*This parses all 12 chapters, generates chunk embeddings, populates ChromaDB, and compiles the BM25 index.*

### 4. Launch the Web Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

### 5. Run the 15-Question Benchmark Suite
```bash
python run_eval.py
```
Automated evaluation reports are generated in `eval_results/`.

---

## 📊 Benchmark Validation Results (100% Score)

| Metric | Target | Benchmark Result | Status |
| :--- | :--- | :--- | :--- |
| **Factual & Multi-Hop Accuracy** | $\ge 90\%$ | **100.0%** (10/10) | ✅ Passed |
| **Refusal / Anti-Hallucination Rate** | $100\%$ | **100.0%** (5/5) | ✅ Passed |
| **Average End-to-End Latency** | $< 8.0\text{s}$ | **1.56s** | ✅ Passed |

---

## 📂 Repository Structure

```
preuniversity-grkraj-org/
├── .streamlit/
│   └── config.toml            # Default Dark Theme configuration
├── corpus/                    # Stored textbook chapters (Markdown)
│   ├── Chapter_01_Plant_Anatomy_and_Tissues.md
│   ├── ...
│   └── Chapter_12_Gene_Expression_Transcription_and_Translation.md
├── chromadb_storage/          # Local Chroma vector database & BM25 index
├── eval_results/              # Automated benchmark reports
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration & model defaults
│   ├── scraper.py             # Chapter scraper & corpus manager
│   ├── ingestion.py           # Text chunking, Chroma embeddings & BM25 indexing
│   ├── hybrid_retriever.py    # BM25 + Dense Chroma retriever with RRF
│   ├── agent_graph.py         # LangGraph state machine with dynamic model execution
│   └── eval_suite.py          # 15-question benchmark dataset
├── app.py                     # Streamlit conversational web dashboard
├── run_eval.py                # Automated evaluation harness
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md                  # Project documentation
```

---

## 📜 Authors & Acknowledgments

- **Knowledge Source**: Prof. Dr. G. R. Kantharaj, Bangalore University ([preuniversity.grkraj.org](https://grkraj.org/pre-university/)).
- **Framework**: Developed for The Gen Academy Agentic AI Program (Week 2 RAG Project).
