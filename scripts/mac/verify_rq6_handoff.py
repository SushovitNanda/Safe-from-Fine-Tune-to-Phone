"""Verify returned M19 labels against delivered ZIPs and central paired inference."""
import hashlib,json,sys,zipfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from analyze_d7 import read
from deployment_stats import paired

def main():
    src=ROOT/'handoff/D7_2026-11-11'
    central=json.loads((src/'laptop_rq6_analysis.json').read_text())['rq6']
    provenance={};labels={}
    for tag in ['stock','protected','random']:
        cell='rep_steer_q3km'+('' if tag=='stock' else '-'+tag)
        d=ROOT/'results/cells'/('mac__'+cell)
        q=read(d/'labels_qwen3guard.jsonl');w=read(d/'labels_wildguard.jsonl');records=read(d/'records.jsonl')
        assert len(q)==len(records)==1612 and len(w)==554
        assert set(q)==set(records) and set(w)=={i for i in q if q[i]['lang']=='hi'}
        labels[tag]={i:{**r,'asr':int(w[i]['harmful_response']=='yes') if i in w else int(r['safety']=='Unsafe'),'orr':int(r['refusal']=='Yes')} for i,r in q.items()}
        if tag=='stock':continue
        info=json.loads((d/'run_info.json').read_text());archive=ROOT/'models/local-results/day8'/info['source_zip']
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==info['sha256_zip']
        with zipfile.ZipFile(archive) as z:raw={r['prompt_id']:r for r in map(json.loads,z.read(info['member']).decode().splitlines())}
        assert set(raw)==set(q)
        for i,r in records.items():
            for field in ['run_fingerprint','stop_token_ids','control_vector','lang','set']:assert r[field]==raw[i][field],(cell,i,field)
            assert r['n_tokens']==raw[i]['token_usage']['completion_tokens']
        provenance[cell]={'zip_sha256':info['sha256_zip'],'exact_1612_ids':True,'fingerprints_settings_tokens_match':True}
    # Central uses original laptop label insertion order. Reproduce that order for an exact check;
    # existing Mac tables retain their frozen dataset order, with finite-bootstrap differences explicit.
    reference=read(ROOT/'results/cells/orig__fp16__f16__tpl-official/labels_qwen3guard.jsonl')
    checks=[]
    for key,a,b in [('protected_minus_stock','protected','stock'),('protected_minus_random','protected','random'),('random_minus_stock','random','stock')]:
        for lang in ['all','en','hi','hinglish']:
            ids=[i for i,r in reference.items() if r['set'].startswith('harmful') and (lang=='all' or r['lang']==lang)]
            local=paired([labels[a][i]['asr']-labels[b][i]['asr'] for i in ids]);expected=central[key][lang]
            assert round(local['difference_pp'],2)==expected['diff']
            assert [round(x,2) for x in local['ci95_pp']]==expected['ci95']
            assert round(local['p_boot'],5)==expected['p']
            checks.append({'contrast':key,'lang':lang,'central_diff_ci_p_reproduced':True})
    result={'provenance':provenance,'central_order_exact_checks':checks,'checks_passed':len(checks),'Mac_order_note':'Primary Mac tables preserve frozen dataset order. Bootstrap CIs/p may differ slightly from central insertion order; point estimates and substantive verdicts agree.','blind_audit_source':'handoff/D7_2026-11-11/README.md; results/review_final/majority_vote.json','H6_supported':False}
    (ROOT/'results/mac/nov11/rq6_handoff_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Both delivered ZIPs/IDs/settings verified; all 12 central ASR contrast estimates, CIs and p-values reproduced exactly')
if __name__=='__main__':main()
