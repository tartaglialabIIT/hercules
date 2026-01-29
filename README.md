# HERCULES

**HERCULES** is a Python package to compute **residue-level RNA-binding propensity**
for proteins from sequence, using a multi-task approach that combines:

- fine-tuned protein language model attention (ProteinBERT)
- physico-chemical amino-acid features

to compute:

- a global RNA-binding propensity score
- a residue-level RNA-binding propensity profile
- a mutational scanning of a protein, predicting the effect of mutations on RNA-binding propensity

---

## 🚀 Installation

First, clone this repository. Then, please use the bash script **install_hercules.sh** to install all the dependencies automatically.

Otherwise follow these instructions to install **Hercules** and its dependencies step-by-step:

0. **Clone the hercules Github repo**

```
git clone https://github.com/tartaglialabIIT/hercules.git
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

6.	**Downloaded trained proteinBERT weights and install Hercules**

```
cd hercules
mkdir -p ~/.cache/hercules/weights
cd ~/.cache/hercules/weights

curl -L -O \
https://github.com/tartaglialabIIT/hercules/releases/download/v1.0.0/proteinbert_weights.tar.gz
tar -xzf proteinbert_weights.tar.gz
```

```
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

📜 **License**

HERCULES is distributed under MIT license

📫 **Contact**

Jonathan Fiorentino & Michele Monti
For questions, issues, or collaborations, please open a GitHub issue
or contact the authors directly.
