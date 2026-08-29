# 🌿 Pre-University Biology AI Tutor (Local Agentic RAG)

A 100% local, agentic Retrieval-Augmented Generation (RAG) tutor for pre-university biology chapters from `preuniversity.grkraj.org`, built with **LangChain**, **LangGraph**, **ChromaDB**, **Ollama**, and **Streamlit**.

---

## 🎯 Features

1. **Hybrid Retrieval**: Combines **BM25 keyword search** (for exact biological names and terminology) with **ChromaDB dense semantic search** merged via **Reciprocal Rank Fusion (RRF)**.
2. **LangGraph Agentic Flow**:
   - **Document Relevance Grading**: Evaluates if retrieved chunks match the query.
   - **Query Rewriting**: Dynamically reformulates search queries if initial retrieval is low-confidence.
   - **Grounded Generation with Citations**: Produces answers citing specific chapters and sections (`[Chapter: Section]`).
   - **Hallucination Guardrail & Safe Refusal**: Gracefully refuses out-of-domain questions with an explicit "I don't know" path rather than hallucinating.
3. **Streamlit Chatbot UI**: Fast conversational interface with citation drawers and parameter controls.
4. **15-Question Automated Evaluation Suite**: Pre-configured benchmark assessing factual accuracy, multi-hop reasoning, and anti-hallucination guardrails.

---

## 🚀 Quickstart (Beginner Step-by-Step)

### Step 1: Install Dependencies
Open PowerShell or your terminal in this directory (`g:\GoogleAntiGravity\local_rag_tutor`):

```bash
uv pip install -r requirements.txt
# OR if using standard pip:
pip install -r requirements.txt
```

### Step 2: Ensure Ollama is Running
Make sure Ollama is active locally. You can pull or run any lightweight local model:
```bash
ollama pull llama3.2
# or
ollama pull gemma2
```

### Step 3: Ingest & Index the Textbook Chapters
Run the ingestion pipeline to scrape/load the chapters, chunk them, and build the local ChromaDB vector store + BM25 index:

```bash
python -m src.ingestion
```

### Step 4: Launch the Streamlit Chatbot UI
Start your conversational web tutor:

```bash
streamlit run app.py
```
This will open your browser at `http://localhost:8501`.

### Step 5: Run the 15-Question Evaluation Suite
Generate your Week 2 Project Deliverable evaluation report:

```bash
python run_eval.py
```
The benchmark report will be generated and saved in `eval_results/`.

---

## 📂 Project Architecture

```
local_rag_tutor/
├── corpus/                    # Stored textbook chapters (Markdown)
├── chromadb_storage/          # Persistent local Chroma vector database & BM25 index
├── src/
│   ├── config.py              # Central settings, chunk sizes, and model parameters
│   ├── scraper.py             # Chapter scraper and corpus loader
│   ├── ingestion.py           # Text splitter, ChromaDB builder & BM25 indexer
│   ├── hybrid_retriever.py    # BM25 + Vector Ensemble with RRF fusion
│   ├── agent_graph.py         # LangGraph stateful agent with relevance grading
│   └── eval_suite.py          # 15-question benchmark dataset
├── app.py                     # Streamlit web chat UI
├── run_eval.py                # Evaluation runner and report generator
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

---

## 📊 Week 2 Project Deliverable Checklist

- [x] **One-Liner Scoped**: High-faithfulness pre-university biology study assistant.
- [x] **Corpus Ingestion & Cleaning**: Structured markdown chapters from `preuniversity.grkraj.org`.
- [x] **Hybrid Retrieval**: BM25 + Dense ChromaDB with Reciprocal Rank Fusion.
- [x] **LangGraph Stateful Graph**: Document grading, query transformation, citation generation, and hallucination checks.
- [x] **Refusal Guardrail**: Deterministic refusal when context is out-of-scope.
- [x] **Conversational UI**: Interactive Streamlit frontend with source inspection.
- [x] **15-Question Evaluation Report**: Automated benchmark covering factual, cross-chapter, and adversarial queries.
