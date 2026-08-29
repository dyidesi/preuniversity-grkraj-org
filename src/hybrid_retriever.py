"""
Hybrid Search Retriever combining Dense ChromaDB Vector Search and Sparse BM25 Keyword Search
via Reciprocal Rank Fusion (RRF).
"""

import pickle
from typing import List, Dict, Tuple
from langchain_core.documents import Document
from langchain_chroma import Chroma

from src.config import (
    CHROMA_DIR,
    TOP_K_DENSE,
    TOP_K_SPARSE,
    TOP_K_FINAL,
    DENSE_WEIGHT,
    SPARSE_WEIGHT
)
from src.ingestion import get_embedding_function, BM25_INDEX_FILE

class HybridRetriever:
    def __init__(self):
        self.embeddings = get_embedding_function()
        self.vectorstore = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=self.embeddings,
            collection_name="preuniversity_biology"
        )
        
        # Load BM25 Index
        if not BM25_INDEX_FILE.exists():
            raise FileNotFoundError(
                f"BM25 index not found at {BM25_INDEX_FILE}. Please run `python -m src.ingestion` first."
            )
        
        with open(BM25_INDEX_FILE, "rb") as f:
            data = pickle.load(f)
            self.bm25 = data["bm25"]
            self.docs = data["docs"]

    def dense_search(self, query: str, k: int = TOP_K_DENSE) -> List[Tuple[Document, float]]:
        """Performs dense semantic similarity search using ChromaDB."""
        results = self.vectorstore.similarity_search_with_relevance_scores(query, k=k)
        return results

    def sparse_search(self, query: str, k: int = TOP_K_SPARSE) -> List[Tuple[Document, float]]:
        """Performs sparse keyword matching using BM25."""
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)
        
        # Pair documents with their BM25 scores
        doc_scores = list(zip(self.docs, scores))
        # Sort descending
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        return doc_scores[:k]

    def hybrid_retrieve(
        self,
        query: str,
        k_final: int = TOP_K_FINAL,
        rrf_constant: int = 60
    ) -> List[Document]:
        """
        Merges dense and sparse search results using Reciprocal Rank Fusion (RRF).
        RRF Score = (Dense_Weight / (rrf_c + dense_rank)) + (Sparse_Weight / (rrf_c + sparse_rank))
        """
        dense_hits = self.dense_search(query, k=TOP_K_DENSE)
        sparse_hits = self.sparse_search(query, k=TOP_K_SPARSE)

        scores_by_id: Dict[str, float] = {}
        doc_by_id: Dict[str, Document] = {}

        # Process Dense Rankings
        for rank, (doc, _) in enumerate(dense_hits):
            chunk_id = doc.metadata.get("chunk_id", doc.page_content[:50])
            doc_by_id[chunk_id] = doc
            scores_by_id[chunk_id] = scores_by_id.get(chunk_id, 0.0) + (DENSE_WEIGHT / (rrf_constant + rank + 1))

        # Process Sparse Rankings
        for rank, (doc, score) in enumerate(sparse_hits):
            if score <= 0.0:
                continue
            chunk_id = doc.metadata.get("chunk_id", doc.page_content[:50])
            doc_by_id[chunk_id] = doc
            scores_by_id[chunk_id] = scores_by_id.get(chunk_id, 0.0) + (SPARSE_WEIGHT / (rrf_constant + rank + 1))

        # Sort combined results
        sorted_ids = sorted(scores_by_id.items(), key=lambda item: item[1], reverse=True)
        
        final_docs = []
        for chunk_id, fusion_score in sorted_ids[:k_final]:
            doc = doc_by_id[chunk_id]
            doc.metadata["fusion_score"] = round(fusion_score, 4)
            final_docs.append(doc)

        return final_docs

if __name__ == "__main__":
    retriever = HybridRetriever()
    test_q = "What is the function of guard cells in stomata?"
    docs = retriever.hybrid_retrieve(test_q, k_final=3)
    print(f"Hybrid Results for '{test_q}':")
    for i, d in enumerate(docs):
        print(f"\n--- Result {i+1} (Score: {d.metadata.get('fusion_score')}) ---")
        print(f"Source: {d.metadata.get('source')} | Section: {d.metadata.get('section_title')}")
        print(d.page_content[:200] + "...")
