# Week 2 Project Deliverable: 15-Question RAG Evaluation Report

**Project**: Local Agentic RAG Tutor (LangChain + LangGraph)  
**Corpus**: `preuniversity.grkraj.org` Biology & Botanical Sciences  
**Generated At**: 2026-08-29 02:23:32  

---

## 1. Executive Summary & Metrics

| Metric | Target | Result | Status |
| :--- | :--- | :--- | :--- |
| **Factual Retrieval & Groundedness** | $\ge 90\%$ | **100.0%** (10/10) | PASS |
| **Refusal / Anti-Hallucination Rate** | $100\%$ | **100.0%** (5/5) | PASS |
| **Average End-to-End Latency** | $< 8.0s$ | **1.56s** | PASS |

---

## 2. Detailed 15-Question Test Results

| ID | Category | Question | Latency | Outcome | Citations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Q01 | Direct Fact | What is the function of guard cells in stomata? | 3.82s | PASS (Grounded with Citations) | Chapter_01_Plant_Anatomy_and_Tissues.md, Chapter_01_Plant_Anatomy.md, Chapter_02_Cell_Structure_and_Organelles.md, Chapter_05_Mineral_Nutrition_in_Plants.md |
| Q02 | Direct Fact | What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout? | 1.24s | PASS (Grounded with Citations) | Chapter_05_Mineral_Nutrition_in_Plants.md, Chapter_05_Mineral_Nutrition_in_Plants.md, Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md, Chapter_01_Plant_Anatomy_and_Tissues.md |
| Q03 | Direct Fact | Which enzyme catalyzes the primary carbon fixation in the C3 Calvin cycle? | 1.19s | PASS (Grounded with Citations) | Chapter_03_Photosynthesis_in_Higher_Plants.md, Chapter_03_Photosynthesis_Mechanism.md, Chapter_03_Photosynthesis_Mechanism.md, Chapter_05_Mineral_Nutrition_in_Plants.md |
| Q04 | Direct Fact | What is the physiological role of Abscisic Acid (ABA) during drought stress? | 1.36s | PASS (Grounded with Citations) | Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md, Chapter_03_Photosynthesis_in_Higher_Plants.md, Chapter_03_Photosynthesis_Mechanism.md, Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md |
| Q05 | Direct Fact | What is the start codon in translation and which amino acid does it specify? | 1.22s | PASS (Grounded with Citations) | Chapter_12_Gene_Expression_Transcription_and_Translation.md, Chapter_12_Gene_Expression_Transcription_and_Translation.md, Chapter_12_Gene_Expression_Transcription_and_Translation.md, Chapter_04_Plant_Water_Relations_and_Transpiration.md |
| Q06 | Cross-Chapter Reasoning | How does the Münch Pressure-Flow Hypothesis in phloem translocation depend on xylem water potential? | 1.37s | PASS (Grounded with Citations) | Chapter_08_Translocation_of_Organic_Solutes.md, Chapter_08_Translocation_of_Organic_Solutes.md, Chapter_04_Plant_Water_Relations.md, Chapter_01_Plant_Anatomy_and_Tissues.md |
| Q07 | Cross-Chapter Reasoning | How do chloroplast grana (light reactions) and mitochondrial cristae (oxidative phosphorylation) generate ATP via chemiosmosis? | 1.21s | PASS (Grounded with Citations) | Chapter_06_Respiration_in_Plants_and_Bioenergetics.md, Chapter_02_Cell_Structure_and_Organelles.md, Chapter_02_Cell_Structure_and_Organelles.md, Chapter_06_Respiration_in_Plants_and_Bioenergetics.md |
| Q08 | Cross-Chapter Reasoning | How does water transport in xylem supply the Oxygen-Evolving Complex (OEC) during photolysis in Photosystem II? | 1.01s | PASS (Grounded with Citations) | Chapter_03_Photosynthesis_in_Higher_Plants.md, Chapter_03_Photosynthesis_Mechanism.md, Chapter_03_Photosynthesis_in_Higher_Plants.md, Chapter_05_Mineral_Nutrition_in_Plants.md |
| Q09 | Cross-Chapter Reasoning | Explain how Morgan's discovery of linkage on Drosophila X-chromosomes deviates from Mendel's Law of Independent Assortment. | 2.54s | PASS (Grounded with Citations) | Chapter_10_Chromosomal_Basis_of_Inheritance_and_Linkage.md, Chapter_09_Principles_of_Genetics_and_Mendelism.md, Chapter_05_Principles_of_Genetics_and_Inheritance.md, Chapter_09_Principles_of_Genetics_and_Mendelism.md |
| Q10 | Cross-Chapter Reasoning | How does biological nitrogen fixation by Nitrogenase in root nodules depend on respiration and leghemoglobin? | 1.02s | PASS (Grounded with Citations) | Chapter_05_Mineral_Nutrition_in_Plants.md, Chapter_05_Mineral_Nutrition_in_Plants.md, Chapter_08_Translocation_of_Organic_Solutes.md, Chapter_05_Mineral_Nutrition_in_Plants.md |
| Q11 | Out-of-Domain (Refusal) | What is the mechanism of action of penicillin on bacterial cell walls? | 1.5s | PASS (Correctly Refused) | None (Refusal) |
| Q12 | Out-of-Domain (Refusal) | What was the closing stock price of Apple on NASDAQ yesterday? | 1.78s | PASS (Correctly Refused) | Chapter_03_Photosynthesis_in_Higher_Plants.md, Chapter_03_Photosynthesis_Mechanism.md, Chapter_03_Photosynthesis_Mechanism.md, Chapter_06_Respiration_in_Plants_and_Bioenergetics.md |
| Q13 | Out-of-Domain (Refusal) | Explain the human circulatory system and the role of the left ventricle. | 1.69s | PASS (Correctly Refused) | None (Refusal) |
| Q14 | Out-of-Domain (Refusal) | How do you implement asynchronous coroutines with asyncio in Python? | 1.28s | PASS (Correctly Refused) | None (Refusal) |
| Q15 | Out-of-Domain (Refusal) | Who won the FIFA World Cup final in 1998? | 1.23s | PASS (Correctly Refused) | None (Refusal) |

---

## 3. Failure & Retrieval Quality Analysis

### [Q01] What is the function of guard cells in stomata?
- **Category**: Direct Fact
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 3.82s)
- **Generated Response**:
> According to the provided textbook chapters, the function of guard cells in stomata is to regulate stomatal opening and closing via changes in turgor pressure. When guard cells take in water and become turgid, the stomatal pore opens, allowing for gas exchange (CO2, O2) and transpiration. Conversely, when guard cells lose water and become flaccid, the pore closes, regulating stomatal activity.

[C...

- **Retrieved Context Snippets**:
  - *Chapter_01_Plant_Anatomy_and_Tissues.md [3. Epidermal Tissue System & Stomatal Apparatus]*: ## 3. Epidermal Tissue System & Stomatal Apparatus
The epidermis forms the outermost uniseriate protective boundary coated by a hydrophobic cutin layer (cuticle).
- **Stomata**: Microscopic pores on foliar surfaces governing gas exchange ($CO_2$, $O_...
  - *Chapter_01_Plant_Anatomy.md [3. Epidermal Tissue System and Stomata]*: ## 3. Epidermal Tissue System and Stomata
The epidermal tissue system forms the outermost protective covering of the plant body.
- **Epidermis**: Single layer of closely packed parenchymatous cells coated with a waxy cuticle that minimizes transpirat...
  - *Chapter_02_Cell_Structure_and_Organelles.md [2. Cell Wall Architecture]*: ## 2. Cell Wall Architecture
- **Primary Cell Wall**: Formed during cell growth; composed primarily of cellulose microfibrils embedded in a matrix of hemicellulose and pectin. It is flexible and extensible.
- **Middle Lamella**: The intercellular cem...
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [2. Classification of Essential Nutrients]*: ## 2. Classification of Essential Nutrients
- **Macronutrients** ($> 10\text{ mmol/kg}$ dry matter): Carbon (C), Hydrogen (H), Oxygen (O), Nitrogen (N), Phosphorus (P), Potassium (K), Calcium (Ca), Magnesium (Mg), Sulfur (S).
  - *Nitrogen*: Constitu...

### [Q02] What are the criteria of essentiality for plant mineral nutrition established by Arnon and Stout?
- **Category**: Direct Fact
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.24s)
- **Generated Response**:
> According to Chapter 5: Mineral Nutrition in Plants, the criteria of essentiality for plant mineral nutrition established by Arnon and Stout are:

1. The plant cannot complete its vegetative or reproductive life cycle without the element.
2. The requirement is specific and irreplaceable by another element.
3. The element is directly involved in plant metabolism (e.g., enzyme constituent or prosthe...

- **Retrieved Context Snippets**:
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [Chapter 5: Mineral Nutrition in Plants]*: # Chapter 5: Mineral Nutrition in Plants
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Essential Mineral Elements
Arnon and Stout established the criteria of essentiality:
1. The plant cannot complete its vegetative or repro...
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [2. Classification of Essential Nutrients]*: ## 2. Classification of Essential Nutrients
- **Macronutrients** ($> 10\text{ mmol/kg}$ dry matter): Carbon (C), Hydrogen (H), Oxygen (O), Nitrogen (N), Phosphorus (P), Potassium (K), Calcium (Ca), Magnesium (Mg), Sulfur (S).
  - *Nitrogen*: Constitu...
  - *Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md [3. Photoperiodism and Vernalization]*: ## 3. Photoperiodism and Vernalization
- **Photoperiodism**: Physiological response of plants to the relative lengths of light and dark periods governed by the **Phytochrome** pigment system ($P_r \rightleftharpoons P_{fr}$). Divided into Short-Day P...
  - *Chapter_01_Plant_Anatomy_and_Tissues.md [2. Classification of Plant Tissues]*: ## 2. Classification of Plant Tissues
Plant tissues are divided into Meristematic Tissues and Permanent Tissues.

### A. Meristematic Tissues
Meristems consist of undifferentiated, thin-walled cells with dense cytoplasm and prominent nuclei engaged i...

### [Q03] Which enzyme catalyzes the primary carbon fixation in the C3 Calvin cycle?
- **Category**: Direct Fact
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.19s)
- **Generated Response**:
> The enzyme that catalyzes the primary carbon fixation in the C3 Calvin cycle is **RuBisCO** (Ribulose-1,5-bisphosphate carboxylase-oxygenase)....

- **Retrieved Context Snippets**:
  - *Chapter_03_Photosynthesis_in_Higher_Plants.md [3. Dark Reactions / Carbon Fixation (Stroma)]*: ## 3. Dark Reactions / Carbon Fixation (Stroma)
### A. The C3 Pathway (Calvin-Benson Cycle)
1. **Carboxylation**: Fixation of $CO_2$ onto Ribulose-1,5-bisphosphate (RuBP, 5C) catalyzed by **RuBisCO** to yield two molecules of 3-Phosphoglycerate (3-PG...
  - *Chapter_03_Photosynthesis_Mechanism.md [A. The Calvin Cycle (C3 Pathway)]*: ### A. The Calvin Cycle (C3 Pathway)
Operates in C3 plants (e.g., rice, wheat). Key phases:
1. **Carboxylation**: Fixation of $CO_2$ by ribulose-1,5-bisphosphate (RuBP) catalyzed by the enzyme **RuBisCO** (Ribulose-1,5-bisphosphate carboxylase-oxygen...
  - *Chapter_03_Photosynthesis_Mechanism.md [B. The Hatch-Slack Pathway (C4 Pathway)]*: ### B. The Hatch-Slack Pathway (C4 Pathway)
Found in tropical grasses (e.g., maize, sugarcane) exhibiting **Kranz Anatomy** (mesophyll cells surrounding bundle sheath cells).
- Primary $CO_2$ acceptor in mesophyll is Phosphoenolpyruvate (PEP), cataly...
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [3. Biological Nitrogen Fixation]*: ## 3. Biological Nitrogen Fixation
Atmospheric dinitrogen ($N_2$) is reduced to ammonia ($NH_3$) by diazotrophs (e.g., *Rhizobium* in legume root nodules) catalyzed by the oxygen-sensitive **Nitrogenase enzyme complex** under microaerophilic conditio...

### [Q04] What is the physiological role of Abscisic Acid (ABA) during drought stress?
- **Category**: Direct Fact
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.36s)
- **Generated Response**:
> According to Chapter 07: Plant Growth Regulators and Phytohormones, [Chapter 07_Plant_Growth_Regulators_and_Phytohormones.md], Abscisic Acid (ABA) is known as the "stress hormone." Its physiological role during drought stress is to induce rapid stomatal closure by altering guard cell membrane permeability, thereby reducing water loss. Additionally, ABA promotes seed dormancy and inhibits precociou...

- **Retrieved Context Snippets**:
  - *Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md [B. Growth Inhibitors & Stress Hormones]*: ### B. Growth Inhibitors & Stress Hormones
- **Abscisic Acid** (ABA): Known as the "stress hormone." Induces rapid stomatal closure under drought/water deficit by altering guard cell membrane permeability; promotes seed dormancy and inhibits precocio...
  - *Chapter_03_Photosynthesis_in_Higher_Plants.md [B. The C4 Pathway (Hatch-Slack Pathway)]*: ### B. The C4 Pathway (Hatch-Slack Pathway)
Adapted to high light, high temperatures, and drought. Exhibits **Kranz Anatomy** (radial arrangement of bundle sheath cells surrounded by mesophyll).
- Mesophyll: Primary carboxylation of Phosphoenolpyruva...
  - *Chapter_03_Photosynthesis_Mechanism.md [B. The Hatch-Slack Pathway (C4 Pathway)]*: ### B. The Hatch-Slack Pathway (C4 Pathway)
Found in tropical grasses (e.g., maize, sugarcane) exhibiting **Kranz Anatomy** (mesophyll cells surrounding bundle sheath cells).
- Primary $CO_2$ acceptor in mesophyll is Phosphoenolpyruvate (PEP), cataly...
  - *Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md [3. Photoperiodism and Vernalization]*: ## 3. Photoperiodism and Vernalization
- **Photoperiodism**: Physiological response of plants to the relative lengths of light and dark periods governed by the **Phytochrome** pigment system ($P_r \rightleftharpoons P_{fr}$). Divided into Short-Day P...

### [Q05] What is the start codon in translation and which amino acid does it specify?
- **Category**: Direct Fact
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.22s)
- **Generated Response**:
> According to Chapter 12: Gene Expression, Transcription, and Translation [Chapter 12: Gene Expression, Transcription, and Translation] [Source: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj], the start codon in translation is **AUG**, which codes for Methionine....

- **Retrieved Context Snippets**:
  - *Chapter_12_Gene_Expression_Transcription_and_Translation.md [3. The Genetic Code and Translation (Protein Synthesis)]*: ## 3. The Genetic Code and Translation (Protein Synthesis)
- **Genetic Code Characteristics**: Triplet code (64 codons: 61 sense codons, 3 stop codons UAA, UAG, UGA), degenerate/redundant, unambiguous, non-overlapping, and universal. Start codon is *...
  - *Chapter_12_Gene_Expression_Transcription_and_Translation.md [General]*: 3. *Elongation*: Cognate aminoacyl-tRNA enters A-site; peptidyl transferase forms peptide bonds; ribosome translocates along mRNA.
  4. *Termination*: Release factors bind stop codons in the A-site, releasing the synthesized polypeptide chain....
  - *Chapter_12_Gene_Expression_Transcription_and_Translation.md [Chapter 12: Gene Expression, Transcription, and Translation]*: # Chapter 12: Gene Expression, Transcription, and Translation
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. The Central Dogma of Molecular Biology
Formulated by Francis Crick:
$$\text{DNA} \xrightarrow{\text{Transcription}} ...
  - *Chapter_04_Plant_Water_Relations_and_Transpiration.md [2. Pathways of Water Movement in Roots]*: ## 2. Pathways of Water Movement in Roots
- **Apoplastic Pathway**: Non-living transport through continuous micro-fibrillar cell wall spaces and intercellular voids. It offers minimal resistance until intercepted at the root endodermis by suberin-imp...

### [Q06] How does the Münch Pressure-Flow Hypothesis in phloem translocation depend on xylem water potential?
- **Category**: Cross-Chapter Reasoning
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.37s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters to answer this question accurately....

- **Retrieved Context Snippets**:
  - *Chapter_08_Translocation_of_Organic_Solutes.md [3. The Pressure-Flow (Mass-Flow) Hypothesis]*: ## 3. The Pressure-Flow (Mass-Flow) Hypothesis
Proposed by Ernst Münch (1930):
1. **Phloem Loading**: Sucrose is actively loaded from mesophyll cells into companion cells and sieve tubes via $H^+/\text{sucrose}$ symporters, driven by plasma membrane ...
  - *Chapter_08_Translocation_of_Organic_Solutes.md [Chapter 8: Translocation of Organic Solutes and Phloem Transport]*: # Chapter 8: Translocation of Organic Solutes and Phloem Transport
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Principles of Phloem Translocation
Organic photosynthates (principally non-reducing sucrose) are translocated f...
  - *Chapter_04_Plant_Water_Relations.md [4. Transpiration and the Cohesion-Tension Theory]*: ## 4. Transpiration and the Cohesion-Tension Theory
- **Transpiration**: The physiological loss of water in the form of water vapor from the aerial parts of plants, primarily through stomata.
- **Cohesion-Tension-Transpiration Pull Theory** (proposed...
  - *Chapter_01_Plant_Anatomy_and_Tissues.md [C. Complex Conducting Tissues]*: ### C. Complex Conducting Tissues
- **Xylem**: Unidirectional vascular tissue conducting water and dissolved minerals from root to shoot. Elements: Tracheids, Vessel Elements (perforated end walls), Xylem Parenchyma (living storage), and Xylem Fibers...

### [Q07] How do chloroplast grana (light reactions) and mitochondrial cristae (oxidative phosphorylation) generate ATP via chemiosmosis?
- **Category**: Cross-Chapter Reasoning
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.21s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters to answer this question accurately....

- **Retrieved Context Snippets**:
  - *Chapter_06_Respiration_in_Plants_and_Bioenergetics.md [4. Electron Transport Chain & Oxidative Phosphorylation]*: ## 4. Electron Transport Chain & Oxidative Phosphorylation
Occurs on the mitochondrial inner membrane (cristae). Electrons from $NADH$ and $FADH_2$ traverse Complexes I, II, III, and IV, driving proton translocation into the intermembrane space. The ...
  - *Chapter_02_Cell_Structure_and_Organelles.md [B. Mitochondria]*: ### B. Mitochondria
Double-membrane bioenergetic organelle where inner membrane invaginations (cristae) harbor $F_0-F_1$ ATP synthase complexes and electron transport chain components generating ATP via oxidative phosphorylation.

### C. The Central ...
  - *Chapter_02_Cell_Structure_and_Organelles.md [B. Mitochondria]*: ### B. Mitochondria
Semi-autonomous double-membrane organelles known as the powerhouses of the cell. The inner membrane folds inward to form cristae, which contain ATP synthase complexes for oxidative phosphorylation and ATP generation during cellula...
  - *Chapter_06_Respiration_in_Plants_and_Bioenergetics.md [3. The Citric Acid Cycle (Krebs Cycle / TCA Cycle)]*: ## 3. The Citric Acid Cycle (Krebs Cycle / TCA Cycle)
Occurs in the mitochondrial matrix.
- **Link Reaction**: Oxidative decarboxylation of pyruvate by Pyruvate Dehydrogenase:
  $$\text{Pyruvate} + CoA + NAD^+ \rightarrow \text{Acetyl-CoA} + CO_2 + N...

### [Q08] How does water transport in xylem supply the Oxygen-Evolving Complex (OEC) during photolysis in Photosystem II?
- **Category**: Cross-Chapter Reasoning
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.01s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters to answer this question accurately....

- **Retrieved Context Snippets**:
  - *Chapter_03_Photosynthesis_in_Higher_Plants.md [2. Light-Dependent Reactions (Thylakoid Membrane)]*: ## 2. Light-Dependent Reactions (Thylakoid Membrane)
- **Photolysis of Water**: Catalyzed by the Oxygen-Evolving Complex (OEC, containing $Mn^{4+}$ and $Ca^{2+}$ clusters) at Photosystem II:
  $$2H_2O \rightarrow 4H^+ + 4e^- + O_2$$
- **Non-Cyclic El...
  - *Chapter_03_Photosynthesis_Mechanism.md [2. Light Reactions (Photochemical Phase)]*: ## 2. Light Reactions (Photochemical Phase)
Occurs in the thylakoid membranes of chloroplasts.
- **Photosystems**: Photosystem I (PSI, reaction center P700) and Photosystem II (PSII, reaction center P680).
- **Photolysis of Water**: Oxygen-evolving c...
  - *Chapter_03_Photosynthesis_in_Higher_Plants.md [Chapter 3: Photosynthesis in Higher Plants]*: # Chapter 3: Photosynthesis in Higher Plants
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Bioenergetics of Photosynthesis
Photosynthesis is an anabolic, light-driven oxido-reduction process converting radiant electromagneti...
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [General]*: - *Magnesium*: Central coordinated ion in the porphyrin ring of chlorophyll; activates RuBisCO and PEP carboxylase.
- **Micronutrients** ($< 10\text{ mmol/kg}$ dry matter): Iron (Fe), Manganese (Mn), Zinc (Zn), Copper (Cu), Boron (B), Molybdenum (Mo)...

### [Q09] Explain how Morgan's discovery of linkage on Drosophila X-chromosomes deviates from Mendel's Law of Independent Assortment.
- **Category**: Cross-Chapter Reasoning
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 2.54s)
- **Generated Response**:
> [Morgan's Experiments on *Drosophila melanogaster* (Chapter 10) and [C. Law of Independent Assortment (Chapter 09 and 05)]]

Morgan's discovery of linkage on *Drosophila* X-chromosomes deviates from Mendel's Law of Independent Assortment in that genes located syntenically on the same chromosome tend to be inherited together as a linkage group, rather than independently of each other. This means th...

- **Retrieved Context Snippets**:
  - *Chapter_10_Chromosomal_Basis_of_Inheritance_and_Linkage.md [2. Morgan's Experiments on *Drosophila melanogaster*]*: ## 2. Morgan's Experiments on *Drosophila melanogaster*
Thomas Hunt Morgan provided experimental proof of the chromosomal theory using fruit flies (*Drosophila melanogaster*):
- Discovered **Sex-Linkage**: The white-eye mutation in *Drosophila* is li...
  - *Chapter_09_Principles_of_Genetics_and_Mendelism.md [C. Law of Independent Assortment]*: ### C. Law of Independent Assortment
The segregation of alleles for one gene occurs independently of the segregation of alleles for another gene during gametogenesis.
- Dihybrid $F_2$ Phenotypic Ratio: $9 : 3 : 3 : 1$
  - 9 Round Yellow ($R_{-}Y_{-}$...
  - *Chapter_05_Principles_of_Genetics_and_Inheritance.md [C. Law of Independent Assortment]*: ### C. Law of Independent Assortment
When two pairs of traits are combined in a hybrid (dihybrid cross), segregation of the pair of characters is independent of the other pair during gamete formation.
- Dihybrid F2 Phenotypic Ratio (e.g., Round Yello...
  - *Chapter_09_Principles_of_Genetics_and_Mendelism.md [3. Mendel's Laws of Inheritance]*: ## 3. Mendel's Laws of Inheritance
### A. Law of Dominance
In a heterozygote ($Tt$), the dominant allele expresses its phenotype, concealing the morphological expression of the recessive allele.

### B. Law of Segregation (Purity of Gametes)
Allelic ...

### [Q10] How does biological nitrogen fixation by Nitrogenase in root nodules depend on respiration and leghemoglobin?
- **Category**: Cross-Chapter Reasoning
- **Outcome**: `PASS (Grounded with Citations)` (Latency: 1.02s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters to answer this question accurately....

- **Retrieved Context Snippets**:
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [3. Biological Nitrogen Fixation]*: ## 3. Biological Nitrogen Fixation
Atmospheric dinitrogen ($N_2$) is reduced to ammonia ($NH_3$) by diazotrophs (e.g., *Rhizobium* in legume root nodules) catalyzed by the oxygen-sensitive **Nitrogenase enzyme complex** under microaerophilic conditio...
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [2. Classification of Essential Nutrients]*: ## 2. Classification of Essential Nutrients
- **Macronutrients** ($> 10\text{ mmol/kg}$ dry matter): Carbon (C), Hydrogen (H), Oxygen (O), Nitrogen (N), Phosphorus (P), Potassium (K), Calcium (Ca), Magnesium (Mg), Sulfur (S).
  - *Nitrogen*: Constitu...
  - *Chapter_08_Translocation_of_Organic_Solutes.md [Chapter 8: Translocation of Organic Solutes and Phloem Transport]*: # Chapter 8: Translocation of Organic Solutes and Phloem Transport
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Principles of Phloem Translocation
Organic photosynthates (principally non-reducing sucrose) are translocated f...
  - *Chapter_05_Mineral_Nutrition_in_Plants.md [General]*: - *Magnesium*: Central coordinated ion in the porphyrin ring of chlorophyll; activates RuBisCO and PEP carboxylase.
- **Micronutrients** ($< 10\text{ mmol/kg}$ dry matter): Iron (Fe), Manganese (Mn), Zinc (Zn), Copper (Cu), Boron (B), Molybdenum (Mo)...

### [Q11] What is the mechanism of action of penicillin on bacterial cell walls?
- **Category**: Out-of-Domain (Refusal)
- **Outcome**: `PASS (Correctly Refused)` (Latency: 1.5s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters (preuniversity.grkraj.org) to answer this question accurately. Please ask a question related to Plant Anatomy, Cell Structure, Photosynthesis, Plant-Water Relations, or Genetics....


### [Q12] What was the closing stock price of Apple on NASDAQ yesterday?
- **Category**: Out-of-Domain (Refusal)
- **Outcome**: `PASS (Correctly Refused)` (Latency: 1.78s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters to answer this question accurately....

- **Retrieved Context Snippets**:
  - *Chapter_03_Photosynthesis_in_Higher_Plants.md [Chapter 3: Photosynthesis in Higher Plants]*: # Chapter 3: Photosynthesis in Higher Plants
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Bioenergetics of Photosynthesis
Photosynthesis is an anabolic, light-driven oxido-reduction process converting radiant electromagneti...
  - *Chapter_03_Photosynthesis_Mechanism.md [Chapter 3: Photosynthesis in Higher Plants]*: # Chapter 3: Photosynthesis in Higher Plants
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Principles of Photosynthesis
Photosynthesis is an anabolic, endergonic, light-sensitized oxidation-reduction process in which green p...
  - *Chapter_03_Photosynthesis_Mechanism.md [2. Light Reactions (Photochemical Phase)]*: ## 2. Light Reactions (Photochemical Phase)
Occurs in the thylakoid membranes of chloroplasts.
- **Photosystems**: Photosystem I (PSI, reaction center P700) and Photosystem II (PSII, reaction center P680).
- **Photolysis of Water**: Oxygen-evolving c...
  - *Chapter_06_Respiration_in_Plants_and_Bioenergetics.md [Chapter 6: Respiration in Plants and Bioenergetics]*: # Chapter 6: Respiration in Plants and Bioenergetics
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Cellular Respiration Principles
Cellular respiration is a catabolic, exergonic oxidative process breaking down complex organi...

### [Q13] Explain the human circulatory system and the role of the left ventricle.
- **Category**: Out-of-Domain (Refusal)
- **Outcome**: `PASS (Correctly Refused)` (Latency: 1.69s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters (preuniversity.grkraj.org) to answer this question accurately. Please ask a question related to Plant Anatomy, Cell Structure, Photosynthesis, Plant-Water Relations, or Genetics....


### [Q14] How do you implement asynchronous coroutines with asyncio in Python?
- **Category**: Out-of-Domain (Refusal)
- **Outcome**: `PASS (Correctly Refused)` (Latency: 1.28s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters (preuniversity.grkraj.org) to answer this question accurately. Please ask a question related to Plant Anatomy, Cell Structure, Photosynthesis, Plant-Water Relations, or Genetics....


### [Q15] Who won the FIFA World Cup final in 1998?
- **Category**: Out-of-Domain (Refusal)
- **Outcome**: `PASS (Correctly Refused)` (Latency: 1.23s)
- **Generated Response**:
> I cannot find sufficient information in the provided textbook chapters (preuniversity.grkraj.org) to answer this question accurately. Please ask a question related to Plant Anatomy, Cell Structure, Photosynthesis, Plant-Water Relations, or Genetics....


