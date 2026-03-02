import pandas as pd
import numpy as np
from .profiles import compute_profile
from joblib import Parallel, delayed
from tqdm.auto import tqdm
import os

AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

def _mutate_position(i, wt_aa, sequence, wt_mean):
    records = []
    for aa in AMINO_ACIDS:
        if aa == wt_aa:
            continue
        mutant = sequence[:i] + aa + sequence[i+1:]
        mut_profile = compute_profile(mutant)
        records.append({
            "position": i + 1,
            "wt": wt_aa,
            "mutant": aa,
            "delta_score": (mut_profile.mean()-wt_mean)/(np.abs(wt_mean)),
        })
    return records

def mutagenesis_scan(sequence: str, n_jobs: int = 1, show_progress: bool = True) -> pd.DataFrame:
    """
    Perform in silico mutagenesis on a single protein sequence.

    Parameters
    ----------
    sequence : str
        Protein sequence
    n_jobs : int
        Number of parallel jobs (-1 to use all cores)
    show_progress : bool
        Show tqdm progress bar

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: position, wt, mutant, delta_score
    """
    wt_profile = compute_profile(sequence)
    wt_mean = wt_profile.mean()

    if n_jobs == -1:
        n_jobs = os.cpu_count() or 1

    positions = list(enumerate(sequence))
    iterator = positions
    if show_progress and n_jobs != 1:
        iterator = tqdm(positions, desc="Mutagenesis scanning")

    results = Parallel(n_jobs=n_jobs)(
        delayed(_mutate_position)(i, aa, sequence, wt_mean)
        for i, aa in iterator
    )

    # Flatten list of lists
    records = [rec for sublist in results for rec in sublist]
    return pd.DataFrame(records)
