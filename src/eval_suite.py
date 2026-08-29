"""
15-Question Evaluation Dataset & Benchmark Harness across all 12 Pre-University Chapters.
"""

from typing import List, Dict

EVAL_BENCHMARK_DATA: List[Dict[str, str]] = [
    # --- Category 1: Direct Factual Questions across Chapters (5 Queries) ---
    {
        "id": "Q01",
        "category": "Direct Fact",
        "question": "What is the function of guard cells in stomata?",
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
        "question": "Which enzyme catalyzes the primary carbon fixation in the C3 Calvin cycle?",
        "expected_type": "answer",
        "expected_topics": ["RuBisCO", "ribulose", "3-PGA", "carboxylation"],
    },
    {
        "id": "Q04",
        "category": "Direct Fact",
        "question": "What is the physiological role of Abscisic Acid (ABA) during drought stress?",
        "expected_type": "answer",
        "expected_topics": ["stress hormone", "stomatal closure", "water deficit", "dormancy"],
    },
    {
        "id": "Q05",
        "category": "Direct Fact",
        "question": "What is the start codon in translation and which amino acid does it specify?",
        "expected_type": "answer",
        "expected_topics": ["AUG", "methionine", "genetic code", "initiation"],
    },

    # --- Category 2: Cross-Chapter & Multi-Document Reasoning (5 Queries) ---
    {
        "id": "Q06",
        "category": "Cross-Chapter Reasoning",
        "question": "How does the Münch Pressure-Flow Hypothesis in phloem translocation depend on xylem water potential?",
        "expected_type": "answer",
        "expected_topics": ["pressure flow", "munch", "sucrose", "osmotic", "xylem", "turgor"],
    },
    {
        "id": "Q07",
        "category": "Cross-Chapter Reasoning",
        "question": "How do chloroplast grana (light reactions) and mitochondrial cristae (oxidative phosphorylation) generate ATP via chemiosmosis?",
        "expected_type": "answer",
        "expected_topics": ["thylakoid", "cristae", "ATP synthase", "chemiosmosis", "proton gradient"],
    },
    {
        "id": "Q08",
        "category": "Cross-Chapter Reasoning",
        "question": "How does water transport in xylem supply the Oxygen-Evolving Complex (OEC) during photolysis in Photosystem II?",
        "expected_type": "answer",
        "expected_topics": ["xylem", "photolysis", "oxygen-evolving", "PSII", "electron donor", "manganese"],
    },
    {
        "id": "Q09",
        "category": "Cross-Chapter Reasoning",
        "question": "Explain how Morgan's discovery of linkage on Drosophila X-chromosomes deviates from Mendel's Law of Independent Assortment.",
        "expected_type": "answer",
        "expected_topics": ["linkage", "recombination", "crossing over", "independent assortment", "dihybrid"],
    },
    {
        "id": "Q10",
        "category": "Cross-Chapter Reasoning",
        "question": "How does biological nitrogen fixation by Nitrogenase in root nodules depend on respiration and leghemoglobin?",
        "expected_type": "answer",
        "expected_topics": ["nitrogenase", "leghemoglobin", "ATP", "rhizobium", "anaerobic"],
    },

    # --- Category 3: Out-of-Domain & Adversarial Refusal Tests (5 Queries) ---
    {
        "id": "Q11",
        "category": "Out-of-Domain (Refusal)",
        "question": "What is the mechanism of action of penicillin on bacterial cell walls?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q12",
        "category": "Out-of-Domain (Refusal)",
        "question": "What was the closing stock price of Apple on NASDAQ yesterday?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q13",
        "category": "Out-of-Domain (Refusal)",
        "question": "Explain the human circulatory system and the role of the left ventricle.",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q14",
        "category": "Out-of-Domain (Refusal)",
        "question": "How do you implement asynchronous coroutines with asyncio in Python?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
    {
        "id": "Q15",
        "category": "Out-of-Domain (Refusal)",
        "question": "Who won the FIFA World Cup final in 1998?",
        "expected_type": "refusal",
        "expected_topics": ["cannot find sufficient information", "not found"],
    },
]
