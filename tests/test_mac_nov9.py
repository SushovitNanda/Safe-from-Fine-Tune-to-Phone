import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/mac'))
from analyze_d7 import holm
from compare_steering_fidelity import compare


def test_fidelity_threshold_and_id_validation():
    ids=[str(i) for i in range(50)]
    ref={i:{'safety':'Safe','refusal':'No'} for i in ids}
    mac={i:dict(r) for i,r in ref.items()}
    mac['0']['safety']='Unsafe';mac['1']['safety']='Unsafe'
    assert compare(mac,ref,ids)['gate_48_of_50_safety']
    mac['2']['safety']='Unsafe'
    assert not compare(mac,ref,ids)['gate_48_of_50_safety']
    with pytest.raises(ValueError,match='exact fixed'):
        compare(mac,ref,ids[:-1])
    mac['3']['safety']='unsure'
    with pytest.raises(ValueError,match='Unresolved'):
        compare(mac,ref,ids)


def test_holm_adjustments_are_monotone_in_rank_and_bounded():
    assert holm([.01,.04,.03])==pytest.approx([.03,.06,.06])
    assert holm([1,0])==[1,0]
