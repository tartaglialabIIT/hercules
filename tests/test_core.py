import numpy as np
from hercules.core import physchem, profiles

SEQ_EXAMPLE = "ACDEFGHIKLMNPQRSTVWY"

def test_transformSecDict():
    dicto = {aa: i for i, aa in enumerate(SEQ_EXAMPLE)}
    result = physchem.transformSecDict(SEQ_EXAMPLE, dicto)
    assert isinstance(result, list)
    assert all(isinstance(x, int) for x in result)

def test_compute_chemphysProfiles():
    scales = ["hercules/core/data/chemphys_scales/charge.json"]
    profiles_arr = physchem.compute_chemphysProfiles(SEQ_EXAMPLE, scales)
    assert isinstance(profiles_arr, np.ndarray)
