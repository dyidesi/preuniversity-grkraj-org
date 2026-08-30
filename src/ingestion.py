"""
Ingestion Pipeline: Document Loading, Chunking, ChromaDB Vector Indexing & BM25 Sparse Indexing.
"""

import pickle
import re
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from rank_bm25 import BM25Okapi

from src.config import (
    CORPUS_DIR,
    CHROMA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL_NAME
)
from src.scraper import sync_corpus

BM25_INDEX_FILE = CHROMA_DIR / "bm25_index.pkl"
DOCS_STORE_FILE = CHROMA_DIR / "processed_docs.pkl"

def get_embedding_function():
    """Initializes local HuggingFace embeddings."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

def extract_section_title(text: str) -> str:
    """Extracts the immediate heading or section title for chunk metadata."""
    headings = re.findall(r'^(#{1,3}\s+.+)$', text, flags=re.MULTILINE)
    return headings[0].replace("#", "").strip() if headings else "General"

def load_documents() -> List[Document]:
    """Loads all Markdown chapters from the corpus directory with metadata."""
    docs = []
    for filepath in sorted(CORPUS_DIR.glob("*.md")):
        text = filepath.read_text(encoding="utf-8")
        
        # Extract main chapter title
        lines = text.splitlines()
        chapter_title = lines[0].replace("#", "").strip() if lines else filepath.stem
        
        doc = Document(
            page_content=text,
            metadata={
                "source": filepath.name,
                "chapter_title": chapter_title,
                "url": f"http://preuniversity.grkraj.org/{filepath.stem}"
            }
        )
        docs.append(doc)
    return docs

def chunk_documents(docs: List[Document]) -> List[Document]:
    """Splits full chapter documents into overlapping, context-rich chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n## ", "\n## ", "\n\n", "\n", " ", ""]
    )
    chunked_docs = []
    for doc in docs:
        splits = splitter.split_text(doc.page_content)
        for i, chunk in enumerate(splits):
            section = extract_section_title(chunk)
            chunked_doc = Document(
                page_content=chunk.strip(),
                metadata={
                    "source": doc.metadata["source"],
                    "chapter_title": doc.metadata["chapter_title"],
                    "section_title": section,
                    "chunk_id": f"{doc.metadata['source']}#chunk_{i}",
                    "url": doc.metadata["url"]
                }
            )
            chunked_docs.append(chunked_doc)
    return chunked_docs

def build_bm25_index(chunked_docs: List[Document]):
    """Builds and serializes BM25 index for sparse keyword search."""
    tokenized_corpus = [doc.page_content.lower().split() for doc in chunked_docs]
    bm25 = BM25Okapi(tokenized_corpus)
    
    with open(BM25_INDEX_FILE, "wb") as f:
        pickle.dump({"bm25": bm25, "docs": chunked_docs}, f)
    print(f"[OK] BM25 Index saved with {len(chunked_docs)} chunks.")

def build_vector_store(chunked_docs: List[Document]) -> Chroma:
    """Builds and persists local ChromaDB vector store."""
    embeddings = get_embedding_function()
    vectorstore = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="preuniversity_biology"
    )
    print(f"[OK] ChromaDB Vector Store indexed {len(chunked_docs)} chunks at {CHROMA_DIR}.")
    return vectorstore

def run_ingestion():
    """Main pipeline execution for data ingestion."""
    print("====================================================")
    print("      LOCAL RAG TUTOR: INGESTION PIPELINE           ")
    print("====================================================")
    
    # 1. Ensure corpus exists
    sync_corpus()
    
    # 2. Load documents
    raw_docs = load_documents()
    print(f"[*] Loaded {len(raw_docs)} full chapter documents.")
    
    # 3. Chunk documents
    chunks = chunk_documents(raw_docs)
    print(f"[*] Created {len(chunks)} chunked documents (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")
    
    # 4. Build BM25 Index
    build_bm25_index(chunks)
    
    # 5. Build Chroma Vector Store
    build_vector_store(chunks)
    
    print("[OK] Ingestion and Indexing complete!\n")

if __name__ == "__main__":
    run_ingestion()
