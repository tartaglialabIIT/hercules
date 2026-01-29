#!/bin/bash
# =============================================================================
# install_hercules.sh
# Robust installation of Hercules and dependencies in a dedicated conda environment
# =============================================================================

set -e  # Exit immediately if any command fails
echo "=========================================="
echo "Starting Hercules installation"
echo "=========================================="

ENV_NAME="hercules"
PYTHON_VERSION="3.8"

# ------------------------
# Step 1: Create Conda environment if it doesn't exist
# ------------------------
if ! conda info --envs | grep -q "^$ENV_NAME"; then
    echo "[1/8] Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
    conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y
else
    echo "[1/8] Conda environment '$ENV_NAME' already exists, skipping creation."
fi

# Ensure conda commands work in script
source "$(conda info --base)/etc/profile.d/conda.sh"

# ------------------------
# Step 2: Install Intel MKL and OpenMP stack
# ------------------------
echo "[2/8] Installing Intel MKL and OpenMP stack..."
conda install -n "$ENV_NAME" -y intel-openmp=2021.4.0 mkl=2021.4.0 -c anaconda

# ------------------------
# Step 3: Install PyTorch (CPU-only)
# ------------------------
echo "[3/8] Installing PyTorch 1.12.1 (CPU-only)..."
conda install -n "$ENV_NAME" -y pytorch=1.12.1 cpuonly -c pytorch

# ------------------------
# Step 4: Install TensorFlow and core Python dependencies
# ------------------------
echo "[4/8] Installing TensorFlow and core Python packages..."
conda run -n "$ENV_NAME" pip install \
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
cd ..
echo "[5/8] Cloning and installing ProteinBERT..."
if [ ! -d "protein_bert" ]; then
    git clone https://github.com/nadavbra/protein_bert.git
fi

conda run -n "$ENV_NAME" bash -c "cd protein_bert && git submodule update --init --recursive && python setup.py install"
cd ..
# ------------------------
# Step 6: Clone and install Hercules
# ------------------------
echo "Downloading proteinBERT weights..."
cd hercules
mkdir -p ~/.cache/hercules/weights
cd ~/.cache/hercules/weights

curl -L -O \
https://github.com/tartaglialabIIT/hercules/releases/download/v1.0.0/proteinbert_weights.tar.gz
tar -xzf proteinbert_weights.tar.gz

echo "[6/8] Installing Hercules..."
conda run -n "$ENV_NAME" bash -c "pip install ."

# ------------------------
# Step 7: Install plotting and progress bar dependencies
# ------------------------
echo "[7/8] Installing matplotlib, seaborn, tqdm..."
conda install -n "$ENV_NAME" -y matplotlib seaborn
conda run -n "$ENV_NAME" pip install tqdm

# ------------------------
# Step 8: Test Hercules installation
# ------------------------
echo "[8/8] Testing Hercules installation..."
conda run -n "$ENV_NAME" python - << EOF
try:
    import hercules
    # simple API call to verify it works
    hercules.api.profiles("MGGKWSKS")
    print("✅ Hercules installation successful")
except Exception as e:
    print("❌ Hercules installation failed")
    raise e
EOF

echo "=========================================="
echo "Hercules installation completed successfully!"
echo "Activate your environment with: conda activate $ENV_NAME"
echo "=========================================="
