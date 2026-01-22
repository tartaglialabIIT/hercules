# hercules/profiles.py
import numpy as np
from .proteinbert import get_attention_profile
from .physchem import load_physchem,compute_chemphysProfiles
from ..models import load_model_generator

alpha = 0.2

_model_generator, _input_encoder, _output_spec = load_model_generator()
_scales, _sel_idx, _weights = load_physchem()

def smooth_profile(vals, fraction=0.05):
    n = len(vals)
    w = max(3, int(n * fraction))
    kernel = np.ones(w) / w
    return np.convolve(vals, kernel, mode="same")

def compute_profile(sequence: str, smooth_fraction: float = 0.05) -> np.ndarray:
    """
    Compute HERCULES profile for a protein sequence, with smoothing and z-normalization.
    
    Parameters
    ----------
    sequence : str
        Protein sequence.
    smooth_fraction : float
        Fraction of sequence length to use for smoothing kernel.
        
    Returns
    -------
    np.ndarray
        Smoothed and z-normalized profile.
    """
    # 1️⃣ Compute raw attention + physchem profile
    attention = get_attention_profile(
        sequence,
        _model_generator,
        _input_encoder
    )
    
    L = len(attention)
    
    physchem = compute_chemphysProfiles(sequence, _scales)
    physchem_sel = physchem[_sel_idx, :]
    combined = np.average(physchem_sel, axis=0, weights=_weights)
    
    profile = L * attention + alpha * combined.mean()
    
    # 2️⃣ Smooth the profile
    profile_smoothed = smooth_profile(profile, fraction=smooth_fraction)
    
    # 3️⃣ z-normalize with fixed mean and std
    mu = 1.0484569
    sigma = 0.47415233
    profile_normalized = (profile_smoothed - mu) / sigma
    
    return profile_normalized
