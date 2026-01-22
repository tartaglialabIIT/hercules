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

Follow these steps to install **Hercules** and its dependencies (use the bash script install_hercules.sh to install all the dependencies automatically):

1. **Create a Conda environment with Python 3.8**

We recommend using Python 3.8, which is fully compatible with ProteinBERT and HERCULES.

```
conda create -n hercules python=3.8 -y
conda activate hercules
```

2. **Force Intel stack first**
```
conda install -y intel-openmp=2021.4.0 mkl=2021.4.0 -c anaconda
```

3. **Install PyTorch from anaconda (NOT conda-forge, NOT pip)**
```
conda install pytorch=1.12.1 cpuonly -c pytorch
```

4. **Install TensorFlow and core dependencies**

Install the versions tested with ProteinBERT 1.0.0:
```
pip install \
  tensorflow==2.13.1 \
  tensorflow-addons==0.21.0 \
  numpy==1.24.3 \
  pandas==2.0.3 \
  h5py==3.11.0 \
  lxml==6.0.2 \
  pyfaidx==0.9.0.3
```

Note
GPU support is optional. For CPU-only systems, the standard TensorFlow package is sufficient.

5. **Clone and install ProteinBERT**

```
git clone https://github.com/nadavbra/protein_bert.git
cd protein_bert
git submodule init
git submodule update
python setup.py install
cd ..
```

Verify the installation:
```
python - << EOF
import proteinbert
print("ProteinBERT installed successfully")
EOF
```

6.	**Clone and install Hercules**

```
git clone https://github.com/tartaglialabIIT/hercules.git
cd hercules
pip install .
```
7. **Install final dependencies**

```
conda install matplotlib seaborn -y
```

```
pip install tqdm
```
8. **Test the installation**

Run a minimal test to verify that HERCULES and ProteinBERT interact correctly:
```
python - << EOF
import hercules
hercules.api.profiles("MGGKWSKS")
print("HERCULES installation successful")
EOF
```

9.	**HERCULES usage**

See the tutorial in the Jupyter notebook for HERCULES usage.

📈 Output interpretation
	•	Higher values indicate higher predicted RNA-binding propensity
	•	Profiles are continuous, not binary
	•	Designed for:
	•	visualization
	•	domain enrichment analysis
	•	comparison across algorithms

🧠 **Method overview**

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


Run tests with:
```
pytest
```

📜 **License**

HERCULES is distributed under XXX license

📫 **Contact**

Jonathan Fiorentino & Michele Monti
For questions, issues, or collaborations, please open a GitHub issue
or contact the authors directly.
