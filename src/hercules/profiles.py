# hercules/profiles.py
import numpy as np
from .attention import calculate_attentions
from .physchem import load_physchem
from .model import load_model_generator
from catgranuleFunctions import compute_chemphysProfiles

alpha = 0.2

_model_generator, _input_encoder = load_model_generator()
_scales, _sel_idx, _weights = load_physchem()

def compute_profile(sequence: str) -> np.ndarray:
    model = _model_generator.create_model(len(sequence) + 2)

    attention = calculate_attentions(model, _input_encoder, sequence)
    L = len(attention)

    physchem = compute_chemphysProfiles(sequence, _scales)
    physchem_sel = physchem[_sel_idx, :]
    combined = np.average(physchem_sel, axis=0, weights=_weights)

    return L * attention + alpha * combined.mean()
