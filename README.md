# HERCULES

**HERCULES** is a Python package to compute **residue-level RNA-binding propensity**
for proteins from sequence, using a multi-task approach that combines:

- fine-tuned protein language model attention (ProteinBERT)
- physico-chemical amino-acid features

to compute:

- a global RNA-binding propensity score
- a residue-level RNA-binding propensity profile
- a mutational scanning of a protein, predicting the effect of mutations on RNA-binding propensity

> **HERCULES is also available as a user-friendly web server at:**  
> https://tools.tartaglialab.com/hercules
---
## ⚙️ System requirements

HERCULES has been tested on Linux (x86_64) systems using Conda environments.

Due to dependencies on specific versions of TensorFlow, PyTorch, and ProteinBERT,
we strongly recommend using the provided installation script and environment.

## 🚀 Installation

First, clone this repository.
For a fully automated setup, we recommend using the provided **install_hercules.sh** script.

```
git clone https://github.com/tartaglialabIIT/hercules.git
cd hercules
chmod +x install_hercules.sh
./install_hercules.sh
```

Alternatively, you can install HERCULES and its dependencies manually by following the steps below.

0. **Clone the hercules Github repo**

```
git clone https://github.com/tartaglialabIIT/hercules.git
cd hercules
```

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

6.	**Download trained proteinBERT weights and install Hercules**
Pretrained weights are not included in the repository and must be downloaded separately.

By default, HERCULES looks for weights in:
```
~/.cache/hercules/weights
```

Download the weights from Zenodo (DOI: 10.5281/zenodo.18413892):
```
mkdir -p ~/.cache/hercules/weights
cd ~/.cache/hercules/weights

curl -fL -o proteinbert_weights.tar.gz \
  https://zenodo.org/records/18413893/files/proteinbert_weights.tar.gz?download=1

tar -xzf proteinbert_weights.tar.gz
```

Then install HERCULES from the cloned repository:
```
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

9. **Using HERCULES in Jupyter**

If you want to run HERCULES in a Jupyter notebook please install the following dependencies:
```
pip install typing-extensions<4.6.0
pip install \
  notebook==6.5.4 \
  traitlets==5.9.0 \
  ipykernel==6.16.2 \
  jupyter-core==4.12.0 \
  jupyter-client==7.4.9
```

Next, add the hercules environment to your jupyter kernels:

```
conda activate hercules
python -m ipykernel install --user --name hercules --display-name "Python (Hercules)"
```

10.	**HERCULES usage**

See the tutorial Jupyter notebook for HERCULES usage.

Run tests with:
```
pytest
```

## 📖 Citation

If you use HERCULES in your work, please cite:

Fiorentino, J.\*, Monti, M.\*, Armaos, A., Miltiadis-Vrachnos, D., Di Rienzo, L., & Tartaglia, G. G.  
**HERCULES: an integrative deep-learning framework for predicting RNA-binding propensity and mutation effects at single-residue resolution**, bioRxiv, 2026  
DOI: https://doi.org/10.64898/2026.03.17.712455

\* These authors contributed equally to this work.

```
@article{fiorentino2026hercules,
  title={HERCULES: an integrative deep-learning framework for predicting RNA-binding propensity and mutation effects at single-residue resolution},
  author={Fiorentino, Jonathan and Monti, Michele and Armaos, Alexandros and Miltiadis-Vrachnos, Dimitrios and Di Rienzo, Lorenzo and Tartaglia, Gian Gaetano},
  journal={bioRxiv},
  pages={2026--03},
  year={2026},
  publisher={Cold Spring Harbor Laboratory}
}
```

📜 **License**

HERCULES is distributed under MIT license.

📫 **Contact**

Jonathan Fiorentino & Michele Monti

For questions, issues, or collaborations, please open a GitHub issue
or contact the authors directly.
