import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus"
CHROMA_DIR = BASE_DIR / "chromadb_storage"
EVAL_RESULTS_DIR = BASE_DIR / "eval_results"

CORPUS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# LLM & Embedding Settings
# Set to Muse Glimmer as requested
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "muse-glimmer-30b:latest")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# Chunking Configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval Configuration
TOP_K_DENSE = 5
TOP_K_SPARSE = 5
TOP_K_FINAL = 4
DENSE_WEIGHT = 0.6
SPARSE_WEIGHT = 0.4
