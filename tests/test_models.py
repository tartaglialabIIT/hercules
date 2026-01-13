import torch
from hercules.models.loaders import load_fusion_model, load_model_generator
from hercules.models.fusion import fused_global_score

def test_load_fusion_model():
    model = load_fusion_model()
    assert isinstance(model, torch.nn.Module)

def test_load_model_generator():
    gen, enc, out_spec = load_model_generator()
    assert gen is not None
    assert enc is not None

def test_fused_global_score():
    seqs = ["MKTFFVAGVILLLSGFSA"]
    df = fused_global_score(seqs)
    assert "HERCULES_global" in df.columns
