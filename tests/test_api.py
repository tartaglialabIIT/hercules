import pytest
from hercules.api import profiles, global_fused_score, mutagenesis

SEQ_EXAMPLE = "MKTFFVAGVILLLSGFSA"
UNIPROT_EXAMPLE = "P69905"  # Human Hemoglobin subunit alpha

def test_from_sequence():
    profile = profiles(SEQ_EXAMPLE)
    assert profile is not None
    assert isinstance(profile, float) or hasattr(profile, "__len__")

def test_from_uniprot(monkeypatch):
    # monkeypatch fetch_sequence to avoid hitting UniProt
    monkeypatch.setattr(
        "hercules.core.sequences.fetch_sequence",
        lambda x: SEQ_EXAMPLE
    )
    profile = profiles(uniprot_ids=UNIPROT_EXAMPLE)
    assert profile is not None

def test_global_fused_score():
    df = global_fused_score([SEQ_EXAMPLE])
    assert "PBERT_global" in df.columns
    assert "PhysChem" in df.columns
    assert "HERCULES_global" in df.columns

def test_mutagenesis():
    df = mutagenesis(SEQ_EXAMPLE)
    assert not df.empty
    assert set(df.columns) >= {"position", "wt", "mutant", "delta_score"}
