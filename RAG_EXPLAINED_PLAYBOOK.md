# 🌿 Pre-University Biology RAG Architecture Playbook
### A Deep-Dive Guide to How This Local Agentic RAG System Works

This playbook provides an end-to-end conceptual and code walkthrough of our local Retrieval-Augmented Generation (RAG) system built over all 12 chapters from `preuniversity.grkraj.org`.

---

## 🏛️ The Complete 7-Stage RAG Stack

```
[ 1. Web Scraping & Ingestion ]  --> 12 Biology Chapters (src/scraper.py)
              │
[ 2. Chunking & Enrichment ]     --> RecursiveCharacterTextSplitter + Section Titles (src/ingestion.py)
              │
[ 3. Dual Indexing ]             --> ChromaDB (Dense Vectors) + BM25Okapi (Sparse Keywords)
              │
[ 4. Hybrid Retrieval & RRF ]    --> Reciprocal Rank Fusion (src/hybrid_retriever.py)
              │
[ 5. LangGraph State Machine ]   --> Document Grading -> Query Rewriter -> Grounded Generator (src/agent_graph.py)
              │
[ 6. Anti-Hallucination Gate ]   --> Factual Grounding Verification & Safe Refusal
              │
[ 7. Conversational UI ]         --> Streamlit Dark Dashboard with Citation Grid (app.py)
```

---

## 1. Step-by-Step Breakdown

### Step 1: Ingestion & Metadata Tagging (`src/scraper.py` & `src/ingestion.py`)
- **Corpus**: 12 structured textbook chapters covering the complete Botany and Molecular Biology curriculum.
- **Cleaning**: Strips navigational markup, scripts, and headers.
- **Metadata**: Each document retains its `source` filename, `chapter_title`, and reference URL (`https://grkraj.org/pre-university/`).

### Step 2: Intelligent Chunking
- **Splitter**: `RecursiveCharacterTextSplitter` configured with `chunk_size=800` characters and `chunk_overlap=150` characters.
- **Hierarchical Enrichment**: For every chunk, regex extracts the immediate subsection heading (`## Section Title`), ensuring that every small excerpt knows its parent chapter and section.

### Step 3 & 4: Dual Indexing (Dense + Sparse)
Most RAG systems fail when querying either exact scientific terms or broad semantic questions. We solve this by maintaining two complementary indices:
1. **Dense Vector Index (`ChromaDB`)**:
   - Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors).
   - Best for: Understanding conceptual intent (e.g. *"how plants absorb water"* $\rightarrow$ matches *"root osmosis & Casparian strip"*).
2. **Sparse Keyword Index (`BM25Okapi`)**:
   - Best for: Exact nomenclature, acronyms, and enzyme names (e.g. *"RuBisCO"*, *"Z-Scheme"*, *"Münch"*, *"9:3:3:1"*).

### Step 5: Hybrid Search with Reciprocal Rank Fusion (RRF)
The `HybridRetriever` queries both indices simultaneously and combines the ranks:

$$\text{RRF Score}(d) = \frac{w_{\text{dense}}}{60 + \text{rank}_{\text{dense}}(d)} + \frac{w_{\text{sparse}}}{60 + \text{rank}_{\text{sparse}}(d)}$$

Where $w_{\text{dense}} = 0.6$ and $w_{\text{sparse}} = 0.4$.

---

## 2. The LangGraph Agentic Workflow

Unlike traditional "naive" RAG (which blindly stuffs top-k chunks into a prompt), our system uses a stateful LangGraph graph with safety guardrails:

```
                  ┌──────────────┐
                  │ 1. RETRIEVE  │ (Hybrid BM25 + Chroma)
                  └──────┬───────┘
                         │
                  ┌──────▼───────┐
                  │ 2. GRADE     │
                  │  DOCUMENTS   │
                  └──────┬───────┘
                         │
         ┌───────────────┴───────────────┐
         │ (Is Relevant?)                │ (Not Relevant & retry < 1)
         ▼                               ▼
  ┌──────────────┐              ┌─────────────────┐
  │ 3. GENERATE  │              │ 3b. REWRITE     │ ──> (Loop back to Retrieve)
  └──────┬───────┘              │     QUERY       │
         │                      └─────────────────┘
  ┌──────▼───────┐
  │ 4. CHECK     │
  │ HALLUCINATION│
  └──────┬───────┘
         │
    ┌────┴────┐
 (Pass)     (Fail)
    ▼         ▼
  [ END ]   [ REFUSAL: "I cannot find sufficient info..." ]
```

---

## 3. Interactive Playbook (`rag_tutorial_playbook.ipynb`)

We have created an interactive Jupyter notebook at:  
👉 [`rag_tutorial_playbook.ipynb`](file:///g:/GoogleAntiGravity/local_rag_tutor/rag_tutorial_playbook.ipynb)

### How to Open & Run the Playbook:

1. **In VS Code**:
   - Open `g:\GoogleAntiGravity\local_rag_tutor\rag_tutorial_playbook.ipynb`.
   - Select the Python kernel: `g:\GoogleAntiGravity\local_rag_tutor\.venv\Scripts\python.exe`.
   - Run cells sequentially to experiment with each stage.

2. **In JupyterLab / Notebook**:
   ```powershell
   cd g:\GoogleAntiGravity\local_rag_tutor
   .\.venv\Scripts\activate
   pip install jupyter
   jupyter notebook rag_tutorial_playbook.ipynb
   ```

---

## 4. Key Takeaways for Production RAG

1. **Chunk size and embedding capacity must match**: 800-character chunks provide sufficient context without diluting 384-dim dense vectors.
2. **Always capture section metadata during chunking**: This allows generating verified chapter citations (`[Chapter 3: Light Reactions]`).
3. **Hybrid search prevents retrieval misses**: Dense handles meaning; BM25 handles exact terms.
4. **Design the refusal path first**: A trustworthy RAG assistant must cleanly refuse out-of-scope queries rather than hallucinating answers.
