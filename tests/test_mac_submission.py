import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/mac'))
from package_redacted_submission import sanitized_label,sanitized_record,FORBIDDEN_KEYS


def test_raw_fields_removed_but_judgments_retained():
    row={'prompt_id':'x','safety':'Unsafe','refusal':'No','response':'PRIVATE','prompt':'PRIVATE','text':'PRIVATE','raw':'PRIVATE','answer':'PRIVATE','input':'PRIVATE'}
    out=sanitized_label(row)
    assert out['safety']=='Unsafe' and out['refusal']=='No'
    assert not FORBIDDEN_KEYS&out.keys() and 'PRIVATE' not in str(out)


def test_text_free_record_keeps_stop_and_vector_provenance_without_local_path():
    r=sanitized_record({'prompt_id':'x','stop_token_ids':[3,6],'control_vector':{'path':'/private/user/file','sha256':'abc','strength':.5,'layer_range':[24,24]},'text':'PRIVATE'})
    assert r['stop_token_ids']==[3,6] and r['control_vector']['sha256']=='abc'
    assert '/private/' not in str(r) and 'text' not in r
