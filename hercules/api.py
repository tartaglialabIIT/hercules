import pandas as pd
from typing import Union, List, Tuple, Dict
from pathlib import Path
from hercules.core.sequences import fetch_sequence
from hercules.core.profiles import compute_profile
from hercules.core.mutagenesis import mutagenesis_scan
from hercules.models.fusion import fused_global_score
from hercules.models.loaders import load_model_generator
from hercules.core.proteinbert import proteinbert_global_score
from functools import lru_cache
from joblib import Parallel, delayed
from tqdm.auto import tqdm
import os

@lru_cache(maxsize=1)
def _get_proteinbert():
    return load_model_generator()

# -------------------------
# helpers
# -------------------------

def _ensure_list(x):
    if isinstance(x, str):
        return [x]
    return list(x)

def _parse_fasta(fasta: str):
    ids, seqs = [], []
    seq = []

    for line in fasta.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if seq:
                seqs.append("".join(seq))
                seq = []
            ids.append(line[1:].split()[0])
        else:
            seq.append(line)

    if seq:
        seqs.append("".join(seq))

    return ids, seqs


def _load_sequences(
    sequences: Union[
        str,
        List[str],
        List[Tuple[str, str]],
        Dict[str, str],
    ] = None,
    uniprot_ids: Union[str, List[str]] = None,
    sequence_ids: Union[str, List[str]] = None,
):
    """
    Load sequences and return (ids, sequences).

    Parameters
    ----------
    sequences : str, list, dict, or list of (id, seq)
        Raw sequences, FASTA path/string, or dict/list with ids
    uniprot_ids : str or list
        UniProt IDs to fetch sequences
    sequence_ids : list
        Optional list of IDs corresponding to sequences (must match length)

    Returns
    -------
    ids : list of str
    sequences : list of str
    """
    if sequences is None and uniprot_ids is None:
        raise ValueError("Provide either sequences or uniprot_ids")

    if sequences is not None and uniprot_ids is not None:
        raise ValueError("Provide only one of sequences or uniprot_ids")

    # ------------------------
    # FASTA input (path or string)
    # ------------------------
    if isinstance(sequences, str):
        if Path(sequences).exists():
            fasta = Path(sequences).read_text()
        elif sequences.lstrip().startswith(">"):
            fasta = sequences
        else:
            # single raw sequence
            seqs = [sequences]
            ids = ["seq_0"] if sequence_ids is None else [sequence_ids]
            return ids, seqs

        return _parse_fasta(fasta)

    # ------------------------
    # Dict: {id: sequence}
    # ------------------------
    if isinstance(sequences, dict):
        return list(sequences.keys()), list(sequences.values())

    # ------------------------
    # List of (id, sequence)
    # ------------------------
    if isinstance(sequences, list) and sequences and isinstance(sequences[0], tuple):
        ids, seqs = zip(*sequences)
        return list(ids), list(seqs)

    # ------------------------
    # List of sequences only
    # ------------------------
    if isinstance(sequences, list):
        if sequence_ids is not None:
            if len(sequence_ids) != len(sequences):
                raise ValueError("Length of sequence_ids must match sequences")
            ids = list(sequence_ids)
        else:
            ids = [f"seq_{i}" for i in range(len(sequences))]
        return ids, sequences

    # ------------------------
    # UniProt IDs
    # ------------------------
    ids = _ensure_list(uniprot_ids)
    seqs = [fetch_sequence(uid) for uid in ids]
    return ids, seqs

# -------------------------
# Public API
# -------------------------

def profiles(
    sequences: Union[str, List[str]] = None,
    uniprot_ids: Union[str, List[str]] = None,
    n_jobs: int = 1,
    show_progress: bool = True,
) -> pd.DataFrame:
    """
    Compute HERCULES RNA-binding profiles.

    Parameters
    ----------
    n_jobs : int
        Number of parallel jobs. Use -1 to use all available cores.
    show_progress : bool
        Show tqdm progress bar.
    """
    ids, seqs = _load_sequences(sequences, uniprot_ids)

    # Serial fallback (default & safest)
    if n_jobs == 1:
        profiles = [compute_profile(seq) for seq in seqs]

    else:
        if n_jobs == -1:
            n_jobs = os.cpu_count() or 1

        iterator = seqs
        if show_progress:
            iterator = tqdm(seqs, desc="Computing HERCULES profiles")

        profiles = Parallel(n_jobs=n_jobs, backend="loky")(
            delayed(compute_profile)(seq) for seq in iterator
        )

    return pd.DataFrame({
        "Protein": ids,
        "Profile": profiles,
    })

def global_fused_score(
    sequences: Union[str, List[str]] = None,
    uniprot_ids: Union[str, List[str]] = None,
) -> pd.DataFrame:
    """
    Compute fused HERCULES global score.
    """
    ids, seqs = _load_sequences(sequences, uniprot_ids)

    df = fused_global_score(seqs, ids=ids)

    # Enforce DataFrame output for public API
    if not isinstance(df, pd.DataFrame):
        raise TypeError("fused_global_score must return a DataFrame")

    return df


def mutagenesis(
    sequence: str = None,
    uniprot_id: str = None,
    n_jobs: int = 1,
    show_progress: bool = True,
) -> pd.DataFrame:
    """
    Perform in silico mutagenesis on a single protein.

    Parameters
    ----------
    sequence : str
        Protein sequence
    uniprot_id : str
        UniProt ID of the protein
    n_jobs : int
        Number of parallel jobs (-1 to use all available cores)
    show_progress : bool
        Show a progress bar during computation

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: position, wt, mutant, delta_score
    """
    if sequence is None and uniprot_id is None:
        raise ValueError("Provide sequence or uniprot_id")

    if sequence is not None and uniprot_id is not None:
        raise ValueError("Provide only one input")

    if uniprot_id is not None:
        sequence = fetch_sequence(uniprot_id)

    # Call the updated scan with parallelization and progress
    return mutagenesis_scan(sequence, n_jobs=n_jobs, show_progress=show_progress)
