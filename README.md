# HERCULES

**HERCULES** is a Python package to compute **residue-level RNA-binding propensity profiles**
for proteins, using a hybrid approach that combines:

- protein language model attention (ProteinBERT)
- physico-chemical amino-acid features
- a supervised, fine-tuned model for RNA-binding prediction

HERCULES can compute profiles from:
- a **protein sequence provided by the user**
- a **UniProt accession**, automatically downloaded

---

## 🚀 Installation

Clone the repository and install locally:

```bash
git clone https://github.com/your-username/hercules.git
cd hercules
pip install .

⚠️ Note
HERCULES relies on proteinbert and tensorflow. GPU is optional but recommended
for large-scale or batch usage.

import hercules

sequence = "MSEQNNTEMTFQIQRIYTKDISFEAPNAPHVFQKDW..."
profile = hercules.from_sequence(sequence)

print(profile.shape)   # (L,)

import hercules

profile = hercules.from_uniprot("P35637")

The returned object is a NumPy array of length L, where L is the protein length.
Each value represents the RNA-binding propensity of the corresponding residue.

📈 Output interpretation
	•	Higher values indicate higher predicted RNA-binding propensity
	•	Profiles are continuous, not binary
	•	Designed for:
	•	visualization
	•	domain enrichment analysis
	•	comparison across algorithms

🧠 Method overview

HERCULES computes RNA-binding propensity as a combination of:
	1.	Attention-based signal
Mean attention over all ProteinBERT global-attention heads.
	2.	Physico-chemical signal
A weighted combination of selected amino-acid scales
learned via elastic-net regression.

The final profile is:
final_profile = L · attention_profile + α · mean_physchem

where:
	•	L is protein length
	•	α is a scaling factor (default: 0.2)

hercules/
├── api.py          # public API
├── profiles.py     # core computation
├── attention.py    # attention extraction
├── physchem.py     # physico-chemical features
├── uniprot.py      # UniProt sequence download
├── model.py        # model loading
└── data/           # model weights and scales

Run tests with:
pytest

Tests are designed to:
	•	check API correctness
	•	avoid long model execution
	•	validate shapes and basic behavior

📜 License

Specify your license here (e.g. MIT, BSD-3, CC-BY-NC, etc.).

📫 Contact

Jonathan Fiorentino & Michele Monti
For questions, issues, or collaborations, please open a GitHub issue
or contact the author directly.
