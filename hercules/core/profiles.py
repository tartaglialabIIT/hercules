# hercules/profiles.py
import numpy as np
from .proteinbert import calculate_attentions
from .physchem import load_physchem,compute_chemphysProfiles
from ..models import load_model_generator

alpha = 0.2

_model_generator, _input_encoder, _output_spec = load_model_generator()
_scales, _sel_idx, _weights = load_physchem()

def compute_profile(sequence: str) -> np.ndarray:
    attention = get_attention_profile(sequence)
    L = len(attention)

    physchem = compute_chemphysProfiles(sequence, _scales)
    physchem_sel = physchem[_sel_idx, :]
    combined = np.average(physchem_sel, axis=0, weights=_weights)

    return L * attention + alpha * combined.mean()
