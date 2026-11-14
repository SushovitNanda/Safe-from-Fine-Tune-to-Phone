"""Compile text-free D8 tables, final RQ6 contrasts and explicit family scopes."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from analyze_d7 import holm
from verify_data import sha256


def main():
    out=ROOT/'reports/D8';out.mkdir(parents=True,exist_ok=True)
    a=json.loads((ROOT/'results/mac/nov11/analysis/deployment_analysis.json').read_text())
    old=json.loads((ROOT/'handoff/D7_2026-11-08/summary.json').read_text())['cells'];new=json.loads((ROOT/'handoff/D7_2026-11-10/summary.json').read_text())['cells']
    core=json.loads((ROOT/'results/final_stats/final.json').read_text())['holm_combined']['tests'];dep=json.loads((ROOT/'handoff/D7_2026-11-10/laptop_gguf_analysis.json').read_text())['holm_deployment']['tests']
    settings=['f16','q4km','q3km','q4km-nopre','budget-phone'];rows=[]
    for s in settings:
        def rate(source,c,key):return source['mac__'+c][key]['rate']
        effect=next(r for r in a['comparisons'] if r['a']=='rep_steer_'+s and r['b']=='med_'+s and (r['metric'],r['subset'],r['lang'])==('asr','pooled','all'))
        ratio=a['retention'].get(s+'|pooled|all')
        rows.append({'setting':s,'medical_ASR':rate(old,'med_'+s,'asr|pooled|all'),'steered_ASR':rate(new,'rep_steer_'+s,'asr|pooled|all'),'steering_difference_pp':effect['difference_pp'],'steering_ci95':effect['ci95_pp'],'retention':ratio,'medical_ORR_general':rate(old,'med_'+s,'over_refusal|benign_general|all'),'steered_ORR_general':rate(new,'rep_steer_'+s,'over_refusal|benign_general|all'),'medical_ORR_clinical':rate(old,'med_'+s,'over_refusal|benign_clinical|all'),'steered_ORR_clinical':rate(new,'rep_steer_'+s,'over_refusal|benign_clinical|all')})
    # Prospectively declared 8 RQ6 ASR contrasts. Do not impute p-values for undelivered labels.
    rq6={}
    for b in ['rep_steer_q3km','rep_steer_q3km-random']:
        for lang in ['all','en','hi','hinglish']:
            key=f"RQ6 protected minus {b} {lang}"
            found=[r for r in a['comparisons'] if r['a']=='rep_steer_q3km-protected' and r['b']==b and (r['metric'],r['subset'],r['lang'])==('asr','pooled',lang)]
            rq6[key]=found[0] if found else {'available':False,'reason':'Central labels for the new M19 pair not delivered'}
    rq6_ready=all('p_boot' in r for r in rq6.values())
    def pval(v):return float(v.get('p',v.get('p_boot')))
    d={f'core:{k}':pval(v) for k,v in core.items()};d.update({f'deployment:{k}':pval(v) for k,v in dep.items()})
    available_holm={k:p for k,p in zip(d,holm(list(d.values())))}
    global_result=None
    if rq6_ready:
        d.update({k:r['p_boot'] for k,r in rq6.items()});global_result={k:p for k,p in zip(d,holm(list(d.values())))}
    source23=json.loads((ROOT/'handoff/D7_2026-11-11/laptop_rq6_analysis.json').read_text())['holm_deployment_with_rq6']
    deployment_p={f'deployment:{k}':pval(v) for k,v in dep.items()}
    deployment_p.update({k:r['p_boot'] for k,r in rq6.items()})
    deployment23={k:p for k,p in zip(deployment_p,holm(list(deployment_p.values())))}
    sources={name:sha256(ROOT/name) for name in ['handoff/D7_2026-11-08/summary.json','handoff/D7_2026-11-10/summary.json','results/mac/nov11/analysis/deployment_analysis.json','results/mac/nov11/d2_med_numeric.json','results/mac/nov11/d2_ctrl_numeric.json','handoff/D7_2026-11-11/laptop_rq6_analysis.json','handoff/D7_2026-11-11/README.md','results/review_final/majority_vote.json','results/mac/nov11/rq6_handoff_verification.json']}
    result={'source_sha256':sources,'rq5_rows':rows,'incoming_laptop_reference_DID_sensitivity':json.loads((ROOT/'handoff/D7_2026-11-10/laptop_gguf_analysis.json').read_text())['gguf']['deltadelta'],'DID_sensitivity_scope':'Supplied mixed-engine/laptop FP16 references for both models; not the unavailable same-engine primary Mac DID','rq6_tests':rq6,'deployment23_Mac_order_holm':deployment23,'deployment23_central_source':source23,'rq6_verdict':{'H6_supported':False,'pooled_interpretation':'No demonstrated protection benefit versus stock or matched random; not equivalence.','english':'Protected is lower than random, surviving the 23-test deployment family, but not different from stock. The 58-test conservative union does not retain that English significance.','hinglish':'Frozen judge scores retained for reproducibility, but blind audit identifies the apparent language contrasts as an artefact on degenerate text; do not interpret as safety effects.','clinical_ORR':'Protected versus stock increases 6.2pp pooled and 13.7pp Hindi; pointwise supporting outcomes, pooled includes directional Hinglish.'},'rq6_central_labels_complete':rq6_ready,'supplied_core_family_size':len(core),'supplied_deployment_family_size':len(dep),'prospective_rq6_family_size':8,'conservative_available_union_holm':available_holm,'complete_union_including_rq6_holm':global_result,'complete_union_size':len(core)+len(dep)+8,'scope_note':'Source core/deployment families retain their declared scopes. Conservative cross-family union is a sensitivity; original registration timing and omissions remain disclosed. All eight RQ6 tests are available; frozen Hinglish scores remain measurement-limited by the blind audit. Retention/NI intervals remain pointwise.'}
    (out/'d8_evidence.json').write_text(json.dumps(result,indent=2)+'\n')
    md=['# D8 tables: labelled RQ5 and RQ6 complete','', '| Setting | Medical ASR | Steered ASR | Change pp [95% CI] | R(s) [95% CI] | Clinical ORR med / steered |','|---|---:|---:|---|---|---|']
    for r in rows:
        q=r['retention'];ratio=f"{q['retention']:.2f} [{q['ci95'][0]:.2f}, {q['ci95'][1]:.2f}]" if q and q.get('available') and q.get('ci95') else 'F16 reference'
        md.append(f"| {r['setting']} | {r['medical_ASR']:.1f} | {r['steered_ASR']:.1f} | {r['steering_difference_pp']:+.2f} [{r['steering_ci95'][0]:+.2f}, {r['steering_ci95'][1]:+.2f}] | {ratio} | {r['medical_ORR_clinical']:.1f} / {r['steered_ORR_clinical']:.1f} |")
    md+=['','ASR denominator:856 harmful prompts/cell; ORR clinical306 benign twins/cell. All intervals pointwise; pooled ORR includes directional Hinglish. All pooled R intervals include1, so H5 is not supported, not proven false. RQ6: H6 is not supported. Pooled protection does not differ from stock or random; this is not equivalence.','',result['scope_note'],'']
    md+=['','## RQ6: primary frozen-label contrasts','', '| Protected minus comparator | Language | Change pp [95% CI] | Raw bootstrap p | Deployment23 Holm p | Conservative58 Holm p |','|---|---|---|---:|---:|---:|']
    for key,r in rq6.items():
        comparator='stock' if r['b']=='rep_steer_q3km' else 'random'
        md.append(f"| {comparator} | {r['lang']} | {r['difference_pp']:+.2f} [{r['ci95_pp'][0]:+.2f}, {r['ci95_pp'][1]:+.2f}] | {r['p_boot']:.4f} | {deployment23[key]:.4f} | {global_result[key]:.4f} |")
    md+=['', 'English protected minus random survives the 23-test deployment family, but not the conservative58-test sensitivity. Protected does not differ from stock in any primary stratum. Hinglish scores are retained as frozen judge outputs, not interpretable safety effects: the targeted blind audit overturned43/44 unsafe labels,39 involving degenerate text. This selected audit is not a replacement full-dataset estimate.', '', 'Protected raises clinical ORR versus stock by6.2pp pooled and13.7pp Hindi. These are supporting pointwise comparisons; pooled ORR includes directional Hinglish. Retention ratios for protected/random use unsteered stock medicalQ3, not unsteered variant counterparts.', '', 'Cross-check: all12 central ASR contrasts reproduced exactly using the central reference-ID order. Mac tables retain frozen dataset order; finite-bootstrap CIs and p-values differ slightly. See results/mac/nov11/rq6_handoff_verification.json.', '']
    (out/'D8_TABLES.md').write_text('\n'.join(md))
    print('D8 RQ5 rows',len(rows),'RQ6 labels complete',rq6_ready,'complete union size',result['complete_union_size'])


if __name__=='__main__':main()
