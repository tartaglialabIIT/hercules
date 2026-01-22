import numpy as np
import pandas as pd
import torch

from hercules.core.proteinbert import proteinbert_global_score
from hercules.core.physchem import load_physchem, compute_chemphysProfiles
from hercules.models.loaders import load_fusion_model, load_model_generator
# ---- load everything ONCE ----
_model_generator, _input_encoder, _output_spec = load_model_generator()
_fusion_nn = load_fusion_model()

_scales, _sel_idx, _weights = load_physchem()


def compute_physchem_mean(sequence: str) -> float:
    profiles = compute_chemphysProfiles(sequence, _scales)
    selected = profiles[_sel_idx, :]
    return np.average(selected.mean(axis=1), weights=_weights)


def fused_global_score(sequences, ids=None):
    if ids is None:
        ids = [f"seq_{i}" for i in range(len(sequences))]

    pb_scores = proteinbert_global_score(
        sequences,
        _model_generator,
        _input_encoder,
        _output_spec
    )

    physchem_means = np.array([
        compute_physchem_mean(seq) for seq in sequences
    ])

    X = torch.tensor(
        np.column_stack([pb_scores, physchem_means]),
        dtype=torch.float32
    )

    with torch.no_grad():
        fused = _fusion_nn(X).cpu().numpy().flatten()

    return pd.DataFrame({
        "Protein": ids,
        "HERCULES_global": fused
    })
