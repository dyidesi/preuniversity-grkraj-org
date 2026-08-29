"""
20-Question Evaluation Dataset & Benchmark Harness across all 12 Pre-University Chapters.
"""

from typing import List, Dict

EVAL_BENCHMARK_DATA: List[Dict[str, str]] = [
    # --- Category 1: Direct Factual Questions across Curriculum (10 Queries) ---
    {
        "id": "Q01",
        "category": "Direct Fact",
        "question": "How do guard cells regulate the opening and closing of stomata?",
        "expected_type": "answer",
        "expected_topics": ["stomata", "turgor pressure", "pore", "transpiration", "epidermal"],
    },
    {
        "id": "Q02",
        "category": "Direct Fact",
        "question": "What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout?",
        "expected_type": "answer",
        "expected_topics": ["essential", "life cycle", "irreplaceable", "metabolism", "Arnon"],
    },
    {
        "id": "Q03",
        "category": "Direct Fact",
        "question": "Explain the three main phases of the Calvin Cycle (C3 pathway) in photosynthesis.",
        "expected_type": "answer",
        "expected_topics": ["RuBisCO", "carboxylation", "reduction", "regeneration", "RuBP"],
    },
    {
        "id": "Q04",
        "category": "Direct Fact",
        "question": "Compare the functions of Auxins in apical dominance with Abscisic Acid (ABA) in drought stress.",
        "expected_type": "answer",
        "expected_topics": ["auxin", "apical dominance", "ABA", "stomatal closure", "stress"],
    },
    {
        "id": "Q05",
        "category": "Direct Fact",
        "question": "What is the start codon in translation and which amino acid does it specify?",
        "expected_type": "answer",
        "expected_topics": ["AUG", "methionine", "genetic code", "initiation"],
    },
    {
        "id": "Q06",
        "category": "Direct Fact",
        "question": "Explain the structural features of the Watson-Crick B-DNA double helix model.",
        "expected_type": "answer",
        "expected_topics": ["double helix", "antiparallel", "base pairing", "hydrogen bonds", "major groove"],
    },
    {
        "id": "Q07",
        "category": "Direct Fact",
        "question": "What is Mendel's Law of Independent Assortment and explain the 9:3:3:1 dihybrid ratio?",
        "expected_type": "answer",
        "expected_topics": ["independent assortment", "dihybrid", "9:3:3:1", "gametes", "alleles"],
    },
    {
        "id": "Q08",
        "category": "Direct Fact",
        "question": "Explain the Cohesion-Tension-Transpiration Pull Theory for water movement in xylem.",
        "expected_type": "answer",
        "expected_topics": ["cohesion", "adhesion", "transpiration pull", "xylem", "water column"],
    },
    {
        "id": "Q09",
        "category": "Direct Fact",
        "question": "What are the structural layers and biochemical components of the plant cell wall?",
        "expected_type": "answer",
        "expected_topics": ["middle lamella", "primary wall", "secondary wall", "cellulose", "pectin"],
    },
    {
        "id": "Q10",
        "category": "Direct Fact",
        "question": "How does Kranz anatomy in C4 plants optimize photosynthetic efficiency and prevent photorespiration?",
        "expected_type": "answer",
        "expected_topics": ["Kranz", "bundle sheath", "mesophyll", "PEP carboxylase", "photorespiration"],
    },

    # --- Category 2: Cross-Chapter & Multi-Document Reasoning (5 Queries) ---
    {
        "id": "Q11",
        "category": "Cross-Chapter Reasoning",
        "question": "How does the Münch Pressure-Flow Hypothesis in phloem translocation depend on xylem water potential?",
        "expected_type": "answer",
        "expected_topics": ["pressure flow", "munch", "sucrose", "osmotic", "xylem", "turgor"],
    },
    {
        "id": "Q12",
        "category": "Cross-Chapter Reasoning",
        "question": "How do chloroplast grana (light reactions) and mitochondrial cristae (oxidative phosphorylation) generate ATP via chemiosmosis?",
        "expected_type": "answer",
        "expected_topics": ["thylakoid", "cristae", "ATP synthase", "chemiosmosis", "proton gradient"],
    },
    {
        "id": "Q13",
        "category": "Cross-Chapter Reasoning",
        "question": "How does water transport in xylem supply the Oxygen-Evolving Complex (OEC) during photolysis in Photosystem II?",
        "expected_type": "answer",
        "expected_topics": ["xylem", "photolysis", "oxygen-evolving", "PSII", "electron donor", "manganese"],
    },
    {
        "id": "Q14",
        "category": "Cross-Chapter Reasoning",
        "question": "Explain how Morgan's discovery of linkage on Drosophila X-chromosomes deviates from Mendel's Law of Independent Assortment.",
        "expected_type": "answer",
        "expected_topics": ["linkage", "recombination", "crossing over", "independent assortment", "dihybrid"],
    },
    {
        "id": "Q15",
        "category": "Cross-Chapter Reasoning",
        "question": "How does biological nitrogen fixation by Nitrogenase in root nodules depend on respiration and leghemoglobin?",
        "expected_type": "answer",
        "expected_topics": ["nitrogenase", "leghemoglobin", "ATP", "rhizobium", "anaerobic"],
    },

    # --- Category 3: Out-of-Domain & Adversarial Refusal Tests (5 Queries) ---
    {
        "id": "Q16",
        "category": "Out-of-Domain (Refusal)",
        "question": "What is the mechanism of action of penicillin on bacterial cell walls?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q17",
        "category": "Out-of-Domain (Refusal)",
        "question": "What was the closing stock price of Apple on NASDAQ yesterday?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q18",
        "category": "Out-of-Domain (Refusal)",
        "question": "Explain the human circulatory system and the role of the left ventricle.",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q19",
        "category": "Out-of-Domain (Refusal)",
        "question": "How do you implement asynchronous coroutines with asyncio in Python?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q20",
        "category": "Out-of-Domain (Refusal)",
        "question": "Who won the FIFA World Cup final in 1998?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
]
