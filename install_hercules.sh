#!/bin/bash
# =============================================================================
# install_hercules.sh
# Install Hercules + dependencies in a dedicated conda environment
# and download model weights from Zenodo.
# =============================================================================

set -euo pipefail

echo "=========================================="
echo "Starting Hercules installation"
echo "=========================================="

ENV_NAME="hercules"
PYTHON_VERSION="3.8"

# --- Always make conda available in non-interactive shells BEFORE using conda ---
source "$(conda info --base)/etc/profile.d/conda.sh"

# Repo root = directory where this script lives (assumes script is in repo root)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ------------------------
# Step 1: Create Conda environment if it doesn't exist
# ------------------------
if ! conda env list | awk '{print $1}' | grep -Fxq "$ENV_NAME"; then
    echo "[1/8] Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
    conda create -n "$ENV_NAME" -y python="$PYTHON_VERSION" pip
else
    echo "[1/8] Conda environment '$ENV_NAME' already exists, skipping creation."
fi

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
conda run -n "$ENV_NAME" python -m pip install -U pip setuptools wheel
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
echo "[5/8] Cloning and installing ProteinBERT..."
cd "$REPO_ROOT/.."
if [ ! -d "protein_bert" ]; then
    git clone https://github.com/nadavbra/protein_bert.git
fi

conda run -n "$ENV_NAME" bash -c "cd '$REPO_ROOT/../protein_bert' && git submodule update --init --recursive && pip install ."

# ------------------------
# Step 6: Download weights from Zenodo and install Hercules
# ------------------------
echo "[6/8] Downloading ProteinBERT weights from Zenodo..."
WEIGHTS_DIR="${HERCULES_WEIGHTS_DIR:-$HOME/.cache/hercules/weights}"
mkdir -p "$WEIGHTS_DIR"
cd "$WEIGHTS_DIR"

# Zenodo direct download (record id comes from DOI 10.5281/zenodo.18413892)
ZENODO_RECORD_ID="18413892"
WEIGHTS_TAR="proteinbert_weights.tar.gz"
WEIGHTS_URL="https://zenodo.org/records/${ZENODO_RECORD_ID}/files/${WEIGHTS_TAR}?download=1"

# Download (fail fast on HTTP errors)
curl -fL -o "$WEIGHTS_TAR" "$WEIGHTS_URL"

# Quick sanity check: file should not be tiny
BYTES=$(wc -c < "$WEIGHTS_TAR" | tr -d ' ')
if [ "$BYTES" -lt 1000000 ]; then
  echo "ERROR: Downloaded weights archive looks too small (${BYTES} bytes)."
  echo "URL was: $WEIGHTS_URL"
  exit 1
fi

# Extract
tar -xzf "$WEIGHTS_TAR"

echo "[6/8] Installing Hercules (from current repo)..."
cd "$REPO_ROOT"
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
conda run -n "$ENV_NAME" python - << 'EOF'
try:
    import hercules
    print("✅ import hercules ok")
except Exception as e:
    print("❌ Hercules installation failed")
    raise
EOF

echo "=========================================="
echo "Hercules installation completed successfully!"
echo "Activate your environment with: conda activate $ENV_NAME"
echo "Weights directory: ${HERCULES_WEIGHTS_DIR:-$HOME/.cache/hercules/weights}"
echo "=========================================="
