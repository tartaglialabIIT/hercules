import warnings
import os
from .plots import plot_profile, plot_mutagenesis_heatmap


# -------------------------------
# Suppress all Python warnings
# -------------------------------
warnings.filterwarnings("ignore")

# -------------------------------
# Optional: suppress TensorFlow logging
# -------------------------------
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # 0=all, 1=info, 2=warnings, 3=errors only

from .api import (
    profiles,
    global_fused_score,
    mutagenesis,
)

__all__ = [
    "profiles",
    "global_fused_score",
    "mutagenesis",
]
