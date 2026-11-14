"""Final research evidence must not confuse family scope or audited judge outputs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def test_final_rq6_evidence_and_family_scopes():
    d=json.loads((ROOT/'reports/D8/d8_evidence.json').read_text())
    assert d['rq6_central_labels_complete'] and len(d['rq6_tests'])==8
    assert len(d['deployment23_Mac_order_holm'])==23
    assert len(d['complete_union_including_rq6_holm'])==d['complete_union_size']==58
    k='RQ6 protected minus rep_steer_q3km-random en'
    assert d['deployment23_Mac_order_holm'][k]<.05
    assert d['complete_union_including_rq6_holm'][k]>.05
    assert not d['rq6_verdict']['H6_supported']
    assert 'artefact' in d['rq6_verdict']['hinglish']
    assert all(r['p_boot']>=1/10000 for r in d['rq6_tests'].values())
    for name,h in d['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h


def test_both_central_imports_verified_before_final_completion():
    d=json.loads((ROOT/'results/mac/nov11/rq6_handoff_verification.json').read_text())
    assert d['checks_passed']==12 and len(d['provenance'])==2
    assert all(r['central_diff_ci_p_reproduced'] for r in d['central_order_exact_checks'])
    assert all(r['exact_1612_ids'] and r['fingerprints_settings_tokens_match'] for r in d['provenance'].values())
