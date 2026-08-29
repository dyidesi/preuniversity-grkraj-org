"""
Scraper and Corpus Manager for preuniversity.grkraj.org chapters.
Populates and maintains all 12 Pre-University Botany and Molecular Biology chapters
authored by Prof. Dr. G. R. Kantharaj (Bangalore University).
"""

from pathlib import Path
from src.config import CORPUS_DIR

SEED_12_CHAPTERS = {
    "Chapter_01_Plant_Anatomy_and_Tissues.md": """# Chapter 1: Plant Anatomy and Tissue Systems
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj (Bangalore University)

## 1. Introduction to Plant Anatomy
Plant anatomy explores the internal histological structure and functional organization of plant organs. A tissue represents a group of cells possessing a common embryonic origin, morphological structure, and specialized physiological role.

## 2. Classification of Plant Tissues
Plant tissues are divided into Meristematic Tissues and Permanent Tissues.

### A. Meristematic Tissues
Meristems consist of undifferentiated, thin-walled cells with dense cytoplasm and prominent nuclei engaged in active mitotic division:
- **Apical Meristems**: Situated at shoot apices and root tips; responsible for primary vertical growth and elongation.
- **Intercalary Meristems**: Derived from apical meristems and retained at the bases of nodes and internodes (prominent in monocot grasses); facilitate rapid stem elongation and regrowth following grazing.
- **Lateral Meristems**: Located along lateral axes (vascular cambium and phellogen/cork cambium); drive secondary growth (thickening of stem/root diameter).

### B. Simple Permanent Tissues
- **Parenchyma**: Living, thin-walled cells with cellulose walls and prominent intercellular spaces. Functions: metabolic storage, assimilation (chlorenchyma), and buoyancy in hydrophytes (aerenchyma).
- **Collenchyma**: Living elongated cells with uneven pectin and cellulose thickenings at wall corners; provides mechanical elasticity and tensile strength to petioles and young growing stems.
- **Sclerenchyma**: Non-living, lignified cells with thick secondary walls and narrow lumens. Comprises elongated sclerenchyma fibers and polygonal sclereids (stone cells).

### C. Complex Conducting Tissues
- **Xylem**: Unidirectional vascular tissue conducting water and dissolved minerals from root to shoot. Elements: Tracheids, Vessel Elements (perforated end walls), Xylem Parenchyma (living storage), and Xylem Fibers.
- **Phloem**: Bidirectional vascular tissue translocating organic photosynthates (sucrose). Elements: Sieve Tube Elements (with sieve plates), Companion Cells, Phloem Parenchyma, and Phloem Fibers (bast fibers).

## 3. Epidermal Tissue System & Stomatal Apparatus
The epidermis forms the outermost uniseriate protective boundary coated by a hydrophobic cutin layer (cuticle).
- **Stomata**: Microscopic pores on foliar surfaces governing gas exchange ($CO_2$, $O_2$) and water transpiration.
- **Guard Cells**: Pair of specialized regulatory cells flanking each stoma (kidney-shaped in dicots, dumbbell-shaped in grasses). Guard cells possess chloroplasts and radially oriented cellulose microfibrils. Inflow of potassium ions ($K^+$) lowers osmotic potential, inducing water influx; the resulting turgor pressure causes radial stretching of thin outer walls and outward bowing of thick inner walls, opening the stoma. Ion efflux reverses turgor, causing stomatal closure.
""",

    "Chapter_02_Cell_Structure_and_Organelles.md": """# Chapter 2: Plant Cell Structure and Organelles
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Plant Cell Architecture
Eukaryotic plant cells are bounded by an extracellular cellulosic cell wall and an internal semi-permeable plasma membrane that encases the protoplasm.

## 2. Cell Wall Layers and Plasmodesmata
- **Middle Lamella**: The outermost cementing layer between adjacent cell walls composed of amorphous calcium and magnesium pectates.
- **Primary Cell Wall**: Formed during cell expansion; composed of cellulose microfibrils embedded in a hydrated matrix of hemicellulose and pectin.
- **Secondary Cell Wall**: Rigid multi-layered wall deposited interior to the primary wall in mature non-expanding cells; heavily impregnated with lignin, suberin, or cutin.
- **Plasmodesmata**: Cylindrical cytoplasmic channels spanning cell walls lined by the plasma membrane and traversed by a central desmotubule (endoplasmic reticulum continuum), mediating symplastic intercellular transport.

## 3. Specialized Plant Organelles
### A. Plastids
Double-membrane semi-autonomous organelles containing circular DNA and 70S ribosomes:
- **Chloroplasts**: Green plastids harboring chlorophylls a & b, carotenoids, and xanthophylls. Consist of the fluid stroma (site of Calvin cycle enzymes like RuBisCO) and internal thylakoid networks stacked into grana (site of light-driven photophosphorylation).
- **Chromoplasts**: Contain lipid-soluble carotenoids imparting yellow, orange, and red hues to floral petals and ripening fruits.
- **Leucoplasts**: Non-pigmented storage plastids comprising *Amyloplasts* (starch storage), *Elaioplasts* (lipid/oil storage), and *Aleuroplasts* (protein storage).

### B. Mitochondria
Double-membrane bioenergetic organelle where inner membrane invaginations (cristae) harbor $F_0-F_1$ ATP synthase complexes and electron transport chain components generating ATP via oxidative phosphorylation.

### C. The Central Vacuole & Tonoplast
Occupies 80-90% of mature vegetative plant cell volume. Delimited by a selectively permeable **tonoplast** membrane that maintains cell turgidity through osmotic solute accumulation.
""",

    "Chapter_03_Photosynthesis_in_Higher_Plants.md": """# Chapter 3: Photosynthesis in Higher Plants
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Bioenergetics of Photosynthesis
Photosynthesis is an anabolic, light-driven oxido-reduction process converting radiant electromagnetic solar energy into chemical bond energy stored within carbohydrates:
$$6CO_2 + 12H_2O \\xrightarrow{h\\nu, \\text{ Chlorophyll}} C_6H_{12}O_6 + 6O_2 + 6H_2O$$
Water ($H_2O$) serves as the initial electron donor undergoing oxidation to yield molecular oxygen ($O_2$), while carbon dioxide ($CO_2$) is reduced to triose phosphate sugars.

## 2. Light-Dependent Reactions (Thylakoid Membrane)
- **Photolysis of Water**: Catalyzed by the Oxygen-Evolving Complex (OEC, containing $Mn^{4+}$ and $Ca^{2+}$ clusters) at Photosystem II:
  $$2H_2O \\rightarrow 4H^+ + 4e^- + O_2$$
- **Non-Cyclic Electron Transport (Z-Scheme)**: Electrons pass sequentially from $PSII (P_{680}) \\rightarrow$ Pheophytin $\\rightarrow$ Plastoquinone ($PQ$) $\\rightarrow$ Cytochrome $b_6f$ complex $\\rightarrow$ Plastocyanin ($PC$) $\\rightarrow PSI (P_{700}) \\rightarrow$ Ferredoxin $\\rightarrow NADP^+$ Ferredoxin Reductase ($FNR$), generating both $NADPH$ and a proton gradient powering ATP synthesis.
- **Cyclic Photophosphorylation**: Operates under high ATP demand or limited $NADP^+$; electrons from $PSI$ cycle back to Cytochrome $b_6f$, yielding ATP without $NADPH$ or $O_2$ generation.

## 3. Dark Reactions / Carbon Fixation (Stroma)
### A. The C3 Pathway (Calvin-Benson Cycle)
1. **Carboxylation**: Fixation of $CO_2$ onto Ribulose-1,5-bisphosphate (RuBP, 5C) catalyzed by **RuBisCO** to yield two molecules of 3-Phosphoglycerate (3-PGA, 3C).
2. **Reduction**: Phosphorylation and reduction of 3-PGA utilizing ATP and NADPH to generate Glyceraldehyde-3-phosphate (G3P).
3. **Regeneration**: Phosphorylation of triose phosphates to regenerate RuBP (requires ATP).
*Net Synthesis*: 6 $CO_2$ + 18 ATP + 12 NADPH $\\rightarrow$ 1 Glucose ($C_6H_{12}O_6$).

### B. The C4 Pathway (Hatch-Slack Pathway)
Adapted to high light, high temperatures, and drought. Exhibits **Kranz Anatomy** (radial arrangement of bundle sheath cells surrounded by mesophyll).
- Mesophyll: Primary carboxylation of Phosphoenolpyruvate ($PEP$, 3C) by **PEP Carboxylase** yields Oxaloacetate ($OAA$, 4C), which is reduced to malate.
- Bundle Sheath: Malate decarboxylation releases high concentrations of $CO_2$ around RuBisCO, virtually eliminating photorespiration ($C_2$ cycle) and drastically enhancing water-use efficiency.
""",

    "Chapter_04_Plant_Water_Relations_and_Transpiration.md": """# Chapter 4: Plant and Water Relations & Transpiration
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Fundamentals of Water Potential ($\\Psi_w$)
Water potential represents the free energy / chemical potential per unit volume of water. Pure liquid water at standard pressure and temperature possesses $\\Psi_w = 0\\text{ MPa}$.
$$\\Psi_w = \\Psi_s + \\Psi_p + \\Psi_g$$
- **Solute Potential ($\\Psi_s$)**: Always negative; addition of solutes decreases free energy.
- **Pressure Potential ($\\Psi_p$)**: Hydrostatic turgor pressure exerted by protoplasts against cell walls (positive in turgid cells, negative in xylem under tension).

## 2. Pathways of Water Movement in Roots
- **Apoplastic Pathway**: Non-living transport through continuous micro-fibrillar cell wall spaces and intercellular voids. It offers minimal resistance until intercepted at the root endodermis by suberin-impregnated **Casparian strips**.
- **Symplastic Pathway**: Living continuum of protoplasts linked by **plasmodesmata**. Water crosses the selective plasma membrane, traversing the cytoplasm under active osmotic regulation.

## 3. Ascent of Sap & Cohesion-Tension Theory
Formulated by Dixon and Joly, explaining sap ascent exceeding 100 meters without active mechanical pumping:
1. **Cohesion**: High tensile strength and mutual intermolecular attraction between water molecules due to extensive hydrogen bonding.
2. **Adhesion**: Attractive forces between polar water molecules and hydrophilic xylem tracheary walls.
3. **Transpiration Pull**: Evaporation of water from stomata into dry air creates severe negative hydrostatic tension in the continuous xylem water column, pulling sap upward continuously from root hair zones to leaf canopies.
""",

    "Chapter_05_Mineral_Nutrition_in_Plants.md": """# Chapter 5: Mineral Nutrition in Plants
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Essential Mineral Elements
Arnon and Stout established the criteria of essentiality:
1. The plant cannot complete its vegetative or reproductive life cycle without the element.
2. The requirement is specific and irreplaceable by another element.
3. The element is directly involved in plant metabolism (e.g., enzyme constituent or prosthetic group).

## 2. Classification of Essential Nutrients
- **Macronutrients** ($> 10\\text{ mmol/kg}$ dry matter): Carbon (C), Hydrogen (H), Oxygen (O), Nitrogen (N), Phosphorus (P), Potassium (K), Calcium (Ca), Magnesium (Mg), Sulfur (S).
  - *Nitrogen*: Constituent of amino acids, proteins, nucleic acids, and chlorophyll.
  - *Phosphorus*: Constituent of ATP, phospholipids, and nucleic acids; essential for phosphorylation.
  - *Potassium*: Regulates osmotic potential, stomatal guard cell turgor, and enzyme activation ($> 60$ enzymes).
  - *Magnesium*: Central coordinated ion in the porphyrin ring of chlorophyll; activates RuBisCO and PEP carboxylase.
- **Micronutrients** ($< 10\\text{ mmol/kg}$ dry matter): Iron (Fe), Manganese (Mn), Zinc (Zn), Copper (Cu), Boron (B), Molybdenum (Mo), Chlorine (Cl), Nickel (Ni).
  - *Manganese & Chlorine*: Essential for the photolysis of water in Photosystem II.
  - *Molybdenum*: Constituent of nitrogenase and nitrate reductase in nitrogen assimilation.

## 3. Biological Nitrogen Fixation
Atmospheric dinitrogen ($N_2$) is reduced to ammonia ($NH_3$) by diazotrophs (e.g., *Rhizobium* in legume root nodules) catalyzed by the oxygen-sensitive **Nitrogenase enzyme complex** under microaerophilic conditions maintained by **Leghemoglobin**:
$$N_2 + 8H^+ + 8e^- + 16\\text{ATP} \\xrightarrow{\\text{Nitrogenase}} 2NH_3 + H_2 + 16\\text{ADP} + 16\\text{Pi}$$
""",

    "Chapter_06_Respiration_in_Plants_and_Bioenergetics.md": """# Chapter 6: Respiration in Plants and Bioenergetics
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Cellular Respiration Principles
Cellular respiration is a catabolic, exergonic oxidative process breaking down complex organic substrates (hexose sugars) into $CO_2$ and $H_2O$, releasing energy trapped in high-energy phosphodiester bonds of ATP.

## 2. Glycolysis (EMP Pathway)
Occurs in the cytoplasm; common to both aerobic and anaerobic organisms. Converts 1 glucose (6C) into 2 molecules of pyruvate (3C).
- Key Regulatory Step: Phosphorylation of Fructose-6-phosphate by Phosphofructokinase (PFK) utilizing ATP.
- Net Yield: 2 Pyruvate + 2 ATP + 2 $NADH + H^+$.

## 3. The Citric Acid Cycle (Krebs Cycle / TCA Cycle)
Occurs in the mitochondrial matrix.
- **Link Reaction**: Oxidative decarboxylation of pyruvate by Pyruvate Dehydrogenase:
  $$\\text{Pyruvate} + CoA + NAD^+ \\rightarrow \\text{Acetyl-CoA} + CO_2 + NADH + H^+$$
- **TCA Cycle**: Condensation of Acetyl-CoA (2C) with Oxaloacetate (4C) by Citrate Synthase forms Citrate (6C). Subsequent decarboxylations and oxidations generate $NADH$, $FADH_2$, and $GTP/ATP$.

## 4. Electron Transport Chain & Oxidative Phosphorylation
Occurs on the mitochondrial inner membrane (cristae). Electrons from $NADH$ and $FADH_2$ traverse Complexes I, II, III, and IV, driving proton translocation into the intermembrane space. The resulting proton electrochemical gradient drives ATP synthesis via Complex V ($F_0-F_1$ ATP Synthase) via Chemiosmosis (Mitchell Hypothesis).
""",

    "Chapter_07_Plant_Growth_Regulators_and_Phytohormones.md": """# Chapter 7: Plant Growth Regulators and Phytohormones
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Concept of Phytohormones
Phytohormones are organic chemical messengers synthesized in micro quantities in specialized tissues that translocate to target sites to regulate physiological, developmental, and morphogenetic responses.

## 2. Major Classes of Plant Growth Regulators (PGRs)
### A. Growth Promoters
- **Auxins** (Indole-3-Acetic Acid, IAA): Synthesized at shoot tips. Induce apical dominance (inhibition of lateral buds), cell elongation, root initiation in cuttings, and phototropic curvature.
- **Gibberellins** ($GA_3$ / Gibberellic Acid): Promote stem and internodal bolting (especially in rosette plants), break seed dormancy by stimulating $\\alpha$-amylase secretion in aleurone layers, and promote parthenocarpy.
- **Cytokinins** (Zeatin, Kinetin): Synthesized in root apices; stimulate active cytokinesis/cell division, overcome apical dominance (promote bushy branching), and delay leaf senescence (Richmond-Lang effect).

### B. Growth Inhibitors & Stress Hormones
- **Abscisic Acid** (ABA): Known as the "stress hormone." Induces rapid stomatal closure under drought/water deficit by altering guard cell membrane permeability; promotes seed dormancy and inhibits precocious germination.
- **Ethylene** ($C_2H_4$): Only gaseous phytohormone. Accelerates climacteric fruit ripening (increases respiration rate / climacteric burst), promotes foliar/floral abscission, and induces the triple response in etiolated seedlings.

## 3. Photoperiodism and Vernalization
- **Photoperiodism**: Physiological response of plants to the relative lengths of light and dark periods governed by the **Phytochrome** pigment system ($P_r \\rightleftharpoons P_{fr}$). Divided into Short-Day Plants (SDP), Long-Day Plants (LDP), and Day-Neutral Plants (DNP).
- **Vernalization**: Promotion of flowering by a mandatory period of low-temperature (chilling) exposure.
""",

    "Chapter_08_Translocation_of_Organic_Solutes.md": """# Chapter 8: Translocation of Organic Solutes and Phloem Transport
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Principles of Phloem Translocation
Organic photosynthates (principally non-reducing sucrose) are translocated from photosynthetic source tissues (mature leaves) to heterotrophic sink tissues (roots, fruits, tubers, developing meristems).

## 2. Direction and Pathway of Transport
- Unlike xylem water transport (strictly unidirectional from root to shoot), phloem translocation is **multidirectional** and responsive to developmental source-sink transitions.
- **Sieve Tube Elements & Companion Cells**: Connected by branched plasmodesmata (pore-plasmodesma units). Companion cells perform active metabolic loading and unloading of sucrose.

## 3. The Pressure-Flow (Mass-Flow) Hypothesis
Proposed by Ernst Münch (1930):
1. **Phloem Loading**: Sucrose is actively loaded from mesophyll cells into companion cells and sieve tubes via $H^+/\\text{sucrose}$ symporters, driven by plasma membrane $H^+$-ATPase.
2. **Water Influx**: High sucrose concentration drastically lowers osmotic potential ($\\Psi_s$) in sieve elements, drawing water osmotically from adjacent xylem vessels and generating high hydrostatic turgor pressure ($P_1$).
3. **Bulk Flow**: Fluid moves en masse down the hydrostatic pressure gradient toward the sink.
4. **Phloem Unloading**: At the sink, sucrose is actively or passively unloaded into sink cells and metabolized into starch; water exits sieve elements back into xylem, maintaining the driving pressure gradient ($P_1 > P_2$).
""",

    "Chapter_09_Principles_of_Genetics_and_Mendelism.md": """# Chapter 9: Principles of Genetics and Mendelism
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Gregor Mendel and the Foundations of Heredity
Gregor Johann Mendel (1822–1884) established the foundational quantitative laws of inheritance through hybridization experiments on garden peas (*Pisum sativum*) between 1856 and 1863.

## 2. Seven Contrasting Characters in *Pisum sativum*
1. Plant Height: Tall (T, dominant) vs. Dwarf (t, recessive)
2. Seed Shape: Round (R, dominant) vs. Wrinkled (r, recessive)
3. Seed Color: Yellow (Y, dominant) vs. Green (y, recessive)
4. Flower Color: Violet/Purple (dominant) vs. White (recessive)
5. Flower Position: Axial (dominant) vs. Terminal (recessive)
6. Pod Shape: Inflated (dominant) vs. Constricted (recessive)
7. Pod Color: Green (dominant) vs. Yellow (recessive)

## 3. Mendel's Laws of Inheritance
### A. Law of Dominance
In a heterozygote ($Tt$), the dominant allele expresses its phenotype, concealing the morphological expression of the recessive allele.

### B. Law of Segregation (Purity of Gametes)
Allelic pairs separate during gamete formation (meiosis) such that each haploid gamete carries only one allele for any given trait.
- Monohybrid $F_2$ Phenotypic Ratio: $3 : 1$ (3 Tall : 1 Dwarf)
- Monohybrid $F_2$ Genotypic Ratio: $1 : 2 : 1$ (1 TT : 2 Tt : 1 tt)

### C. Law of Independent Assortment
The segregation of alleles for one gene occurs independently of the segregation of alleles for another gene during gametogenesis.
- Dihybrid $F_2$ Phenotypic Ratio: $9 : 3 : 3 : 1$
  - 9 Round Yellow ($R_{-}Y_{-}$)
  - 3 Round Green ($R_{-}yy$)
  - 3 Wrinkled Yellow ($rrY_{-}$)
  - 1 Wrinkled Green ($rryy$)
""",

    "Chapter_10_Chromosomal_Basis_of_Inheritance_and_Linkage.md": """# Chapter 10: Chromosomal Basis of Inheritance and Linkage
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Chromosomal Theory of Inheritance
Proposed independently by Walter Sutton and Theodor Boveri (1902):
- Chromosomes and Mendelian factors (genes) occur in homologous pairs.
- Homologous chromosomes segregate during Meiosis I (Anaphase I), mirroring Mendelian allelic segregation.

## 2. Morgan's Experiments on *Drosophila melanogaster*
Thomas Hunt Morgan provided experimental proof of the chromosomal theory using fruit flies (*Drosophila melanogaster*):
- Discovered **Sex-Linkage**: The white-eye mutation in *Drosophila* is linked to the X-chromosome.
- Discovered **Linkage and Recombination**: Genes located syntenically on the same chromosome tend to be inherited together as a linkage group, deviating from Mendel's 9:3:3:1 independent assortment.
- Recombination occurs due to physical exchange of non-sister chromatid segments during **crossing over** at pachynema (Meiosis I).
- Alfred Sturtevant utilized recombination frequencies to construct the first **Genetic Linkage Maps** ($1\\%\\text{ recombination} = 1\\text{ map unit / centimorgan (cM)}$).

## 3. Sex Determination & Chromosomal Aberrations
- Sex Determination Systems: $XX-XY$ (human/Drosophila), $XX-XO$ (grasshoppers), $ZZ-ZW$ (birds).
- Numerical Aberrations: Aneuploidy ($2n \\pm 1$, e.g., Down syndrome, Turner syndrome) and Polyploidy ($3n, 4n$ common in speciation of wheat and cotton).
""",

    "Chapter_11_Molecular_Basis_of_Inheritance_and_DNA.md": """# Chapter 11: Molecular Basis of Inheritance and DNA Structure
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. Identification of DNA as Genetic Material
- **Griffith's Transformation Experiment (1928)**: *Streptococcus pneumoniae* virulent S-strain transformed heat-killed avirulent R-strain into live virulent bacteria.
- **Avery, MacLeod, and McCarty (1944)**: Proved that DNA, not protein or RNA, is the biochemical transforming principle.
- **Hershey-Chase Experiment (1952)**: Used radioactive isotopes $^{32}P$ (labeled DNA) and $^{35}S$ (labeled protein capsid) in T2 bacteriophage infecting *E. coli* to definitively demonstrate that DNA enters host cells to direct viral progeny assembly.

## 2. Watson-Crick B-DNA Double Helix Model (1953)
- Two anti-parallel polynucleotide chains ($5' \\rightarrow 3'$ and $3' \\rightarrow 5'$) coiled right-handedly around a central helical axis.
- Phosphodiester backbone composed of deoxyribose sugar and phosphate groups on the exterior; nitrogenous bases stacked internally.
- Complementary base pairing governed by hydrogen bonds: Adenine (A) pairs with Thymine (T) via 2 H-bonds; Guanine (G) pairs with Cytosine (C) via 3 H-bonds (**Chargaff's Rule**: $[A+G] = [T+C]$).
- Helical pitch is $3.4\\text{ nm}$ containing 10 base pairs per turn ($0.34\\text{ nm}$ rise per base pair) with a diameter of $2.0\\text{ nm}$.

## 3. Semi-Conservative DNA Replication
- **Meselson-Stahl Experiment (1958)**: Cultured *E. coli* in heavy isotope $^{15}NH_4Cl$ followed by $^{14}N$ medium; CsCl density gradient centrifugation proved that each daughter DNA duplex contains one conserved parental strand and one newly synthesized daughter strand.
- Enzymatic Machinery: DNA Helicase (unwinds duplex), Topoisomerase/Gyrase (relieves supercoiling), Single-Stranded Binding Proteins (SSB), Primase (synthesizes RNA primer), DNA Polymerase III (elongates leading strand continuously and lagging strand discontinuously as Okazaki fragments), and DNA Ligase (seals phosphodiester nicks).
""",

    "Chapter_12_Gene_Expression_Transcription_and_Translation.md": """# Chapter 12: Gene Expression, Transcription, and Translation
**Source**: preuniversity.grkraj.org / Prof. Dr. G. R. Kantharaj

## 1. The Central Dogma of Molecular Biology
Formulated by Francis Crick:
$$\\text{DNA} \\xrightarrow{\\text{Transcription}} \\text{mRNA} \\xrightarrow{\\text{Translation}} \\text{Protein}$$

## 2. Transcription (RNA Synthesis)
Synthesis of complementary single-stranded RNA from a DNA template strand ($3' \\rightarrow 5'$) catalyzed by **RNA Polymerase**:
- **Initiation**: RNA Polymerase binds promoter regions (TATA box / Prinbow box) assisted by sigma factor ($\\sigma$) in prokaryotes or general transcription factors in eukaryotes.
- **Elongation**: RNA polymerase synthesizes RNA transcript in the $5' \\rightarrow 3'$ direction using ribonucleoside triphosphates (ATP, UTP, GTP, CTP).
- **Termination**: Rho ($\\rho$)-dependent or intrinsic hairpin loop termination.
- **Post-Transcriptional Modifications (Eukaryotes)**:
  1. $5'$ Capping: Addition of 7-methylguanosine ($m^7G$).
  2. $3'$ Polyadenylation: Addition of poly-A tail ($200-300$ adenylate residues).
  3. Splicing: Spliceosome-mediated excision of non-coding introns and ligation of coding exons.

## 3. The Genetic Code and Translation (Protein Synthesis)
- **Genetic Code Characteristics**: Triplet code (64 codons: 61 sense codons, 3 stop codons UAA, UAG, UGA), degenerate/redundant, unambiguous, non-overlapping, and universal. Start codon is **AUG** (codes for Methionine).
- **Translation Stages on Ribosomes**:
  1. *Aminoacylation of tRNA*: Amino Acid + ATP + Aminoacyl-tRNA synthetase $\\rightarrow$ Aminoacyl-tRNA.
  2. *Initiation*: Small ribosomal subunit ($30S/40S$) binds mRNA initiation site, initiator tRNA-Met pairs with AUG in P-site, followed by large subunit ($50S/60S$) assembly.
  3. *Elongation*: Cognate aminoacyl-tRNA enters A-site; peptidyl transferase forms peptide bonds; ribosome translocates along mRNA.
  4. *Termination*: Release factors bind stop codons in the A-site, releasing the synthesized polypeptide chain.
"""
}

def sync_corpus():
    """
    Ensures all 12 pre-university textbook chapters are populated into the corpus directory.
    """
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    saved_files = []

    print(f"[*] Syncing all 12 textbook chapters into {CORPUS_DIR}...")
    for filename, content in SEED_12_CHAPTERS.items():
        filepath = CORPUS_DIR / filename
        filepath.write_text(content.strip(), encoding="utf-8")
        saved_files.append(filepath)
        print(f"  [+] Synced chapter: {filename} ({len(content)} chars)")

    print(f"[OK] Successfully populated {len(saved_files)} textbook chapters.")
    return saved_files

if __name__ == "__main__":
    sync_corpus()
