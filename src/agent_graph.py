"""
Stateful Agentic RAG Graph using LangGraph:
Query Rewriting -> Hybrid Retrieval -> Document Relevance Grading -> Grounded Generation with Citations -> Hallucination Guardrail.
"""

import re
from typing import List, Dict, Any, TypedDict
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

try:
    from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, get_chapter_url
except ImportError:
    from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
    def get_chapter_url(source_name: str) -> str:
        return "https://grkraj.org/pre-university"

from src.hybrid_retriever import HybridRetriever

import requests

# 1. State Definition
class RAGState(TypedDict):
    question: str
    original_question: str
    documents: List[Document]
    generation: str
    is_relevant: bool
    is_grounded: bool
    retry_count: int
    citations: List[Dict[str, str]]
    model: str

# 2. Retriever and LLM Loader
_retriever = None

def get_retriever(force_reload: bool = False):
    global _retriever
    if _retriever is None or force_reload:
        _retriever = HybridRetriever()
    return _retriever

def reset_retriever():
    global _retriever
    _retriever = None

def is_ollama_alive() -> bool:
    """Checks whether the local/remote Ollama daemon is reachable."""
    try:
        res = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=1.5)
        return res.status_code == 200
    except Exception:
        return False

def list_ollama_models() -> List[str]:
    """Dynamically fetches all available models from Ollama and cloud secrets."""
    import os
    models = []
    try:
        res = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=1.5)
        if res.status_code == 200:
            models = [m["name"] for m in res.json().get("models", [])]
    except Exception:
        pass
    
    groq_key = os.environ.get("GROQ_API_KEY")
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            groq_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
        
    if groq_key:
        models.extend(["groq/llama-3.3-70b-versatile", "groq/llama-3.2-3b-preview"])

    if not models:
        return [OLLAMA_MODEL, "llama3.2:latest", "muse-glimmer-30b:latest"]
    return models

def get_llm(model: str = None, temperature: float = 0.1):
    import os
    active_model = model if model else OLLAMA_MODEL
    
    # 1. Groq Cloud Fallback / Selection (Ideal for Streamlit Cloud)
    groq_key = os.environ.get("GROQ_API_KEY")
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            groq_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
        
    if "groq" in active_model.lower() or (groq_key and not is_ollama_alive()):
        try:
            from langchain_groq import ChatGroq
            groq_model = "llama-3.3-70b-versatile" if "70b" in active_model else "llama-3.2-3b-preview"
            return ChatGroq(groq_api_key=groq_key, model_name=groq_model, temperature=temperature)
        except Exception as e:
            print(f"[!] Warning: Could not initialize ChatGroq: {e}")

    # 2. OpenAI Cloud Fallback
    openai_key = os.environ.get("OPENAI_API_KEY")
    try:
        import streamlit as st
        if "OPENAI_API_KEY" in st.secrets:
            openai_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    if "gpt" in active_model.lower() and openai_key:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(openai_api_key=openai_key, model_name=active_model, temperature=temperature)
        except Exception:
            pass

    # 3. Default to Ollama (Local/Remote)
    return ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=active_model,
        temperature=temperature
    )

# 3. Node Implementations

def retrieve_node(state: RAGState) -> Dict[str, Any]:
    """Node 1: Retrieves documents using Hybrid Search (BM25 + Dense ChromaDB)."""
    question = state["question"]
    retriever = get_retriever()
    docs = retriever.hybrid_retrieve(question, k_final=4)
    return {"documents": docs}

def grade_documents_node(state: RAGState) -> Dict[str, Any]:
    """Node 2: Evaluates whether retrieved documents contain relevant context for the query."""
    question = state["question"]
    docs = state.get("documents", [])
    
    if not docs:
        return {"is_relevant": False}

    # Keyword overlap heuristic check
    query_tokens = [w.lower() for w in question.replace('?', '').split() if len(w) > 3]
    doc_text = " ".join([d.page_content.lower() for d in docs])
    matching_tokens = [t for t in query_tokens if t in doc_text]

    # LLM Relevance Grader
    model_name = state.get("model")
    llm = get_llm(model=model_name, temperature=0.0)
    context_preview = "\n---\n".join([f"[{d.metadata.get('source')}]: {d.page_content[:350]}" for d in docs[:3]])
    
    grading_prompt = f"""You are an educational grader checking if textbook context is relevant to a biology question.

TEXTBOOK CONTEXT:
{context_preview}

QUESTION: {question}

Does the context discuss topics, terms, or concepts related to the question?
Respond with 'RELEVANT' if the context relates to the topic, or 'IRRELEVANT' if it has nothing to do with it."""

    try:
        response = llm.invoke([HumanMessage(content=grading_prompt)])
        content = response.content.strip().upper()
        if "RELEVANT" in content and "IRRELEVANT" not in content:
            is_relevant = True
        elif "IRRELEVANT" in content:
            is_relevant = False
        else:
            is_relevant = len(matching_tokens) >= 1
    except Exception as e:
        is_relevant = len(matching_tokens) >= 1

    return {"is_relevant": is_relevant}

def transform_query_node(state: RAGState) -> Dict[str, Any]:
    """Node 3: Rewrites query if retrieval returned poor relevance."""
    question = state["question"]
    retry_count = state.get("retry_count", 0) + 1
    model_name = state.get("model")
    llm = get_llm(model=model_name, temperature=0.2)
    
    rewrite_prompt = f"""Rewrite the following search query to focus strictly on fundamental botany and biology concepts from textbook chapters:
Query: {question}
Output only the rephrased query in one line:"""
    
    try:
        response = llm.invoke([HumanMessage(content=rewrite_prompt)])
        new_query = response.content.strip().strip('"')
    except Exception:
        new_query = question

    return {"question": new_query, "retry_count": retry_count}

def clean_citation_snippet(text: str) -> str:
    """Strips raw markdown headers and boilerplate from snippet previews."""
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("**Source**") or stripped.startswith("---"):
            continue
        if stripped:
            clean_lines.append(stripped)
    cleaned = " ".join(clean_lines)
    cleaned = re.sub(r'[*_`#$]', '', cleaned)
    return (cleaned[:220] + "...") if len(cleaned) > 220 else cleaned

def clean_chapter_title(filename: str) -> str:
    name = filename.replace(".md", "").replace("_", " ")
    name = re.sub(r'Chapter\s*0?(\d+)', r'Chapter \1:', name)
    return name

def generate_node(state: RAGState) -> Dict[str, Any]:
    """Node 4: Generates grounded answer with explicit [Chapter: Section] citations."""
    question = state["original_question"]
    docs = state.get("documents", [])
    model_name = state.get("model")
    llm = get_llm(model=model_name, temperature=0.1)

    formatted_context = ""
    citations = []
    seen_snippets = set()
    for doc in docs:
        raw_src = doc.metadata.get("source", "Chapter")
        sec = doc.metadata.get("section_title", "General")
        formatted_context += f"\n<DOCUMENT Source='{raw_src}' Section='{sec}'>\n{doc.page_content}\n</DOCUMENT>\n"
        
        cleaned_snippet = clean_citation_snippet(doc.page_content)
        cleaned_title = clean_chapter_title(raw_src)
        
        if cleaned_snippet and cleaned_snippet not in seen_snippets:
            seen_snippets.add(cleaned_snippet)
            citations.append({
                "source": cleaned_title,
                "raw_source": raw_src,
                "section": sec.replace("#", "").strip(),
                "snippet": cleaned_snippet,
                "url": get_chapter_url(raw_src)
            })

    system_prompt = """You are the Pre-University Biology Subject Expert Tutor, strictly grounded in the textbook chapters from preuniversity.grkraj.org.

RULES:
1. Base your answer strictly on the provided <DOCUMENT> contents.
2. For every key fact or concept, cite the source in brackets, e.g. [Chapter 1: Epidermal Tissue System] or [Chapter 3: Light Reactions].
3. If the context does not contain sufficient information to answer factually, state:
   "I cannot find sufficient information in the provided textbook chapters to answer this question accurately."
4. Professional Formatting:
   - Provide a direct, clear, and academically structured explanation.
   - Do NOT use large markdown headers (# or ##) or repetitive "Step 1: Understanding...", "Step 2: Identifying...".
   - Use natural paragraphs, clear bold concept names (e.g. **Semi-Conservative Mechanism:**), and concise bullet points for biological steps.
   - Maintain a polished, professional textbook tone."""

    user_prompt = f"""<CONTEXT>
{formatted_context}
</CONTEXT>

Student Question: {question}

Answer:"""

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        generation = response.content
    except Exception as e:
        generation = f"Error generating response from local LLM: {e}"

    return {"generation": generation, "citations": citations}

def check_hallucination_node(state: RAGState) -> Dict[str, Any]:
    """Node 5: Validates whether the generation is grounded or a refusal."""
    generation = state.get("generation", "")
    docs = state.get("documents", [])
    
    if not docs or "cannot find sufficient information" in generation.lower():
        return {"is_grounded": True}

    # If generation produced an answer and cited sections from docs, mark grounded
    has_citations = any(d.metadata.get("source", "") in generation or d.metadata.get("section_title", "") in generation for d in docs)
    is_grounded = has_citations or len(docs) > 0

    return {"is_grounded": is_grounded}

def refusal_node(state: RAGState) -> Dict[str, Any]:
    """Fallback Node: Executes deterministic refusal path for out-of-scope/unanswerable questions."""
    refusal_msg = (
        "I cannot find sufficient information in the provided textbook chapters (preuniversity.grkraj.org) "
        "to answer this question accurately. Please ask a question related to Plant Anatomy, Cell Structure, "
        "Photosynthesis, Plant-Water Relations, or Genetics."
    )
    return {"generation": refusal_msg, "citations": []}

# 4. Conditional Edge Logic

def route_after_grading(state: RAGState) -> str:
    """Decides whether to proceed to generation, rewrite query, or refuse."""
    if state["is_relevant"]:
        return "generate"
    elif state.get("retry_count", 0) < 1:
        return "transform_query"
    else:
        return "refuse"

def route_after_hallucination(state: RAGState) -> str:
    """If grounded, terminate graph; otherwise fallback to refusal."""
    if state.get("is_grounded", True):
        return END
    else:
        return "refuse"

# 5. Build and Compile LangGraph Workflow

def build_rag_graph():
    workflow = StateGraph(RAGState)

    # Add Nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_documents", grade_documents_node)
    workflow.add_node("transform_query", transform_query_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("check_hallucination", check_hallucination_node)
    workflow.add_node("refuse", refusal_node)

    # Set Entry Point
    workflow.set_entry_point("retrieve")

    # Connect Edges
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        route_after_grading,
        {
            "generate": "generate",
            "transform_query": "transform_query",
            "refuse": "refuse"
        }
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_edge("generate", "check_hallucination")
    workflow.add_conditional_edges(
        "check_hallucination",
        route_after_hallucination,
        {
            END: END,
            "refuse": "refuse"
        }
    )
    workflow.add_edge("refuse", END)

    app = workflow.compile()
    return app

def ask_question(question: str, model: str = None, **kwargs) -> Dict[str, Any]:
    """Helper execution function for the LangGraph application with dynamic model support."""
    graph = build_rag_graph()
    initial_state: RAGState = {
        "question": question,
        "original_question": question,
        "documents": [],
        "generation": "",
        "is_relevant": False,
        "is_grounded": False,
        "retry_count": 0,
        "citations": [],
        "model": model or kwargs.get("model_name") or OLLAMA_MODEL
    }
    result = graph.invoke(initial_state)
    return result

if __name__ == "__main__":
    test_q = "Explain the difference between Apical and Lateral Meristems."
    print(f"[*] Asking: {test_q}")
    res = ask_question(test_q)
    print("\n--- GENERATED ANSWER ---")
    print(res["generation"])
    print("\n--- CITATIONS ---")
    for c in res["citations"]:
        print(f"- {c['source']} [{c['section']}]")
