#!/bin/bash
# =============================================================================
# install_hercules.sh
# Install Hercules and its dependencies in a dedicated conda environment
# =============================================================================

set -e  # Exit immediately if a command exits with a non-zero status
echo "=========================================="
echo "Starting Hercules installation"
echo "=========================================="

ENV_NAME="hercules"
PYTHON_VERSION="3.8"

# ------------------------
# Step 1: Create Conda environment
# ------------------------
echo "[1/8] Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y
echo "Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

# ------------------------
# Step 2: Force Intel stack first
# ------------------------
echo "[2/8] Installing Intel MKL and OpenMP stack..."
conda install -y intel-openmp=2021.4.0 mkl=2021.4.0 -c anaconda

# ------------------------
# Step 3: Install PyTorch (CPU-only)
# ------------------------
echo "[3/8] Installing PyTorch 1.12.1 (CPU-only) from Anaconda..."
conda install pytorch=1.12.1 cpuonly -c pytorch -y

# ------------------------
# Step 4: Install TensorFlow and core dependencies
# ------------------------
echo "[4/8] Installing TensorFlow 2.13.1 and core dependencies..."
pip install \
  tensorflow==2.13.1 \
  tensorflow-addons==0.21.0 \
  numpy==1.24.3 \
  pandas==2.0.3 \
  h5py==3.11.0 \
  lxml==6.0.2 \
  pyfaidx==0.9.0.3

# ------------------------
# Step 5: Clone and install ProteinBERT
# ------------------------
echo "[5/8] Cloning ProteinBERT repository..."
if [ ! -d "protein_bert" ]; then
    git clone https://github.com/nadavbra/protein_bert.git
fi
cd protein_bert
echo "Initializing submodules..."
git submodule init
git submodule update
echo "Installing ProteinBERT..."
python setup.py install
cd ..

# Verify ProteinBERT
echo "Verifying ProteinBERT installation..."
python - << EOF
try:
    import proteinbert
    print("ProteinBERT installed successfully ✅")
except Exception as e:
    print("ProteinBERT installation failed ❌")
    raise e
EOF

# ------------------------
# Step 6: Clone and install Hercules
# ------------------------
echo "[6/8] Cloning Hercules repository..."
if [ ! -d "hercules" ]; then
    git clone https://github.com/tartaglialabIIT/hercules.git
fi
cd hercules
echo "Installing Hercules..."
pip install .
cd ..

# ------------------------
# Step 7: Install plotting and progress bar dependencies
# ------------------------
echo "[7/8] Installing final dependencies: matplotlib, seaborn, tqdm..."
conda install matplotlib seaborn -y
pip install tqdm

# ------------------------
# Step 8: Test Hercules installation
# ------------------------
echo "[8/8] Testing Hercules installation..."
python - << EOF
try:
    import hercules
    hercules.api.profiles("MGGKWSKS")
    print("HERCULES installation successful ✅")
except Exception as e:
    print("HERCULES installation failed ❌")
    raise e
EOF

echo "=========================================="
echo "Hercules installation completed successfully!"
echo "Activate your environment with: conda activate $ENV_NAME"
echo "=========================================="
