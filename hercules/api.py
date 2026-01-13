import pandas as pd
from typing import Union, List

from hercules.core.sequences import fetch_sequence
from hercules.core.profiles import compute_profile
from hercules.core.mutagenesis import mutagenesis_scan
from hercules.models.fusion import fused_global_score
from hercules.models.loaders import load_model_generator
from hercules.core.proteinbert import proteinbert_global_score


# -------------------------
# helpers
# -------------------------

def _ensure_list(x):
    if isinstance(x, str):
        return [x]
    return list(x)


def _load_sequences(
    sequences: Union[str, List[str]] = None,
    uniprot_ids: Union[str, List[str]] = None,
):
    if sequences is None and uniprot_ids is None:
        raise ValueError("Provide either sequences or uniprot_ids")

    if sequences is not None and uniprot_ids is not None:
        raise ValueError("Provide only one of sequences or uniprot_ids")

    if sequences is not None:
        seqs = _ensure_list(sequences)
        ids = [f"seq_{i}" for i in range(len(seqs))]
        return ids, seqs

    ids = _ensure_list(uniprot_ids)
    seqs = [fetch_sequence(uid) for uid in ids]
    return ids, seqs


# -------------------------
# Public API
# -------------------------

def profiles(
    sequences: Union[str, List[str]] = None,
    uniprot_ids: Union[str, List[str]] = None,
) -> pd.DataFrame:
    """
    Compute HERCULES RNA-binding profiles.
    """
    ids, seqs = _load_sequences(sequences, uniprot_ids)

    profiles = [compute_profile(seq) for seq in seqs]

    return pd.DataFrame({
        "Protein": ids,
        "Profile": profiles
    })


def global_proteinbert_score(
    sequences: Union[str, List[str]] = None,
    uniprot_ids: Union[str, List[str]] = None,
) -> pd.DataFrame:
    """
    Compute ProteinBERT global RNA-binding scores.
    """
    ids, seqs = _load_sequences(sequences, uniprot_ids)

    model_generator, input_encoder, output_spec = load_model_generator()
    scores = proteinbert_global_score(
        seqs, model_generator, input_encoder, output_spec
    )

    return pd.DataFrame({
        "Protein": ids,
        "PBERT_global": scores
    })


def global_fused_score(
    sequences: Union[str, List[str]] = None,
    uniprot_ids: Union[str, List[str]] = None,
) -> pd.DataFrame:
    """
    Compute fused HERCULES global score.
    """
    ids, seqs = _load_sequences(sequences, uniprot_ids)
    return fused_global_score(seqs, ids=ids)


def mutagenesis(
    sequence: str = None,
    uniprot_id: str = None,
) -> pd.DataFrame:
    """
    Perform in silico mutagenesis on a single protein.
    """
    if sequence is None and uniprot_id is None:
        raise ValueError("Provide sequence or uniprot_id")

    if sequence is not None and uniprot_id is not None:
        raise ValueError("Provide only one input")

    if uniprot_id is not None:
        sequence = fetch_sequence(uniprot_id)

    return mutagenesis_scan(sequence)
