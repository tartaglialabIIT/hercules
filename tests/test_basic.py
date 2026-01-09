import numpy as np
import pytest
import hercules

def test_from_sequence_runs():
    """Basic sanity check: profile from sequence."""
    seq = "MSEQNNTEMTFQIQRIYTKDISFEAPNAPHVFQKDW"
    profile = hercules.from_sequence(seq)

    assert isinstance(profile, np.ndarray)
    assert profile.ndim == 1
    assert len(profile) == len(seq)


def test_from_uniprot_runs(monkeypatch):
    """Mock UniProt download to avoid network dependency."""

    fake_seq = "ACDEFGHIKLMNPQRSTVWY"

    def mock_fetch(uniprot_id):
        return fake_seq

    monkeypatch.setattr(
        "hercules.uniprot.fetch_sequence",
        mock_fetch
    )

    profile = hercules.from_uniprot("P00000")

    assert isinstance(profile, np.ndarray)
    assert len(profile) == len(fake_seq)


def test_profile_is_finite():
    """Ensure no NaNs or infs in output."""
    seq = "ACDEFGHIKLMNPQRSTVWY"
    profile = hercules.from_sequence(seq)

    assert np.all(np.isfinite(profile))
