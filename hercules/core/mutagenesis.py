import pandas as pd
from .profiles import compute_profile
from joblib import Parallel, delayed
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
            "delta_score": wt_mean - mut_profile.mean(),
        })
    return records

def mutagenesis_scan(sequence):
    wt_profile = compute_profile(sequence)
    wt_mean = wt_profile.mean()

    n_cores = os.cpu_count() or 2

    # Parallel over positions (joblib handles batching efficiently)
    results = Parallel(n_jobs=n_cores)(
        delayed(_mutate_position)(i, aa, sequence, wt_mean) 
        for i, aa in enumerate(sequence)
    )

    # Flatten list of lists
    records = [rec for sublist in results for rec in sublist]
    return pd.DataFrame(records)
