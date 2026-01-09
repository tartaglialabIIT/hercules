# hercules/api.py
from .profiles import compute_profile
from .uniprot import fetch_sequence

def from_sequence(sequence: str):
    return compute_profile(sequence)

def from_uniprot(uniprot_id: str):
    seq = fetch_sequence(uniprot_id)
    return compute_profile(seq)
