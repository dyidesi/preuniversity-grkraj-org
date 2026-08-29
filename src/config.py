import os
import re
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
# Set to Llama 3.2 as default model
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
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

# Direct Live Chapter URL Mapping on grkraj.org
CHAPTER_URL_MAP = {
    "Chapter_01_Plant_Anatomy_and_Tissues.md": "https://grkraj.org/chapters/pre-university/3_PLANT_ANATOMY.htm",
    "Chapter_02_Cell_Structure_and_Organelles.md": "https://grkraj.org/chapters/pre-university/1_CELL_STRUCTURE.htm",
    "Chapter_03_Photosynthesis_in_Higher_Plants.md": "https://grkraj.org/chapters/pre-university/7_PHOTOSYNTHESIS.htm",
    "Chapter_04_Plant_Water_Relations_and_Transpiration.md": "https://grkraj.org/chapters/pre-university/4_PLANT_AND_WATER_RELATIONSHIP.htm",
    "Chapter_05_Mineral_Nutrition_in_Plants.md": "https://grkraj.org/chapters/pre-university/6_PLANT_GROWTH_AND_DEVELOPMENT.htm",
    "Chapter_06_Respiration_in_Plants_and_Bioenergetics.md": "https://grkraj.org/chapters/pre-university/8_RESPIRATION.htm",
    "Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md": "https://grkraj.org/chapters/pre-university/6_PLANT_GROWTH_AND_DEVELOPMENT.htm",
    "Chapter_08_Translocation_of_Organic_Solutes.md": "https://grkraj.org/chapters/pre-university/5_TRANSLOCATION_OF_ORGANIC_SOLUTES.htm",
    "Chapter_09_Principles_of_Genetics_and_Mendelism.md": "https://grkraj.org/chapters/pre-university/9_GENETICS.htm",
    "Chapter_10_Chromosomal_Basis_of_Inheritance_and_Linkage.md": "https://grkraj.org/chapters/pre-university/9_GENETICS.htm",
    "Chapter_11_Molecular_Basis_of_Inheritance_and_DNA.md": "https://grkraj.org/chapters/pre-university/10_MOLECULAR_BIOLOGY.htm",
    "Chapter_12_Gene_Expression_Transcription_and_Translation.md": "https://grkraj.org/chapters/pre-university/10_MOLECULAR_BIOLOGY.htm",
}

def get_chapter_url(source_name: str) -> str:
    """Resolves any filename, chapter title, or source tag to its direct live chapter URL on grkraj.org."""
    source_clean = str(source_name).strip()
    # 1. Exact or partial filename match
    for filename, url in CHAPTER_URL_MAP.items():
        if filename.lower() in source_clean.lower() or filename.replace(".md", "").lower() in source_clean.lower():
            return url
    
    # 2. Match by chapter number (e.g. Chapter 5 or Ch. 05)
    match = re.search(r'Chapter\s*0?(\d+)', source_clean, re.IGNORECASE)
    if match:
        num = int(match.group(1))
        num_map = {
            1: "https://grkraj.org/chapters/pre-university/3_PLANT_ANATOMY.htm",
            2: "https://grkraj.org/chapters/pre-university/1_CELL_STRUCTURE.htm",
            3: "https://grkraj.org/chapters/pre-university/7_PHOTOSYNTHESIS.htm",
            4: "https://grkraj.org/chapters/pre-university/4_PLANT_AND_WATER_RELATIONSHIP.htm",
            5: "https://grkraj.org/chapters/pre-university/6_PLANT_GROWTH_AND_DEVELOPMENT.htm",
            6: "https://grkraj.org/chapters/pre-university/8_RESPIRATION.htm",
            7: "https://grkraj.org/chapters/pre-university/6_PLANT_GROWTH_AND_DEVELOPMENT.htm",
            8: "https://grkraj.org/chapters/pre-university/5_TRANSLOCATION_OF_ORGANIC_SOLUTES.htm",
            9: "https://grkraj.org/chapters/pre-university/9_GENETICS.htm",
            10: "https://grkraj.org/chapters/pre-university/9_GENETICS.htm",
            11: "https://grkraj.org/chapters/pre-university/10_MOLECULAR_BIOLOGY.htm",
            12: "https://grkraj.org/chapters/pre-university/10_MOLECULAR_BIOLOGY.htm",
        }
        if num in num_map:
            return num_map[num]
            
    return "https://grkraj.org/pre-university"
