"""After M16/M17 finish, verify corrected v2 exports with fixed calibration checks.

Waits in 30-second increments so it does not compete for GPU during full cells.
Publishes only to the dedicated Manish branch. No safety judging is performed.
"""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from run_cell import digest
from verify_data import sha256
LOCAL=ROOT/'models/local-results/day7'
OUT=ROOT/'results/mac/nov10'


def main():
    while True:
        state=json.loads((LOCAL/'SESSION_STATE.json').read_text())
        if state['status']=='failed':raise RuntimeError('Full-cell pipeline failed; resolve it before operational checks')
        if state['status']=='complete':
            command=subprocess.run(['ps','-p',str(state['pid']),'-o','command='],capture_output=True,text=True).stdout
            if 'run_steering_cells.py' not in command:break
        time.sleep(30)
    report=json.loads((OUT/'medical_d4_v2_protection.json').read_text());missing={f'blk.0.{m}.weight' for m in ['ffn_gate','ffn_up','ffn_down']}
    if missing & (report['protected_rules'].keys()|report['random_rules'].keys()):raise ValueError('Excluded attribution re-entered candidate pool')
    if not report['matched_random_size_exact']:raise ValueError('Unmatched builds')
    frozen=json.loads((ROOT/'configs/mac/planning/m13_runcheck100.json').read_text());checks={}
    for tag in ['protected','random']:
        model=ROOT/f'models/gguf/medical-d4-v2/{tag}-q3km.gguf'
        if sha256(model)!=report['builds'][tag]['sha256']:raise ValueError('Corrected model changed')
        log=LOCAL/f'd4-v2-{tag}.server.log';receipt=log.with_suffix('.receipt.json');receipt.unlink(missing_ok=True)
        with (LOCAL/f'd4-v2-{tag}.launcher.log').open('a') as f:
            server=subprocess.Popen([sys.executable,str(ROOT/'scripts/mac/serve.py'),'--gguf',str(model),'--stop-eot','--log',str(log)],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
            try:
                for _ in range(240):
                    if server.poll() is not None:raise RuntimeError('Corrected server failed')
                    if receipt.exists():break
                    time.sleep(1)
                else:raise TimeoutError('Server receipt timeout')
                path=LOCAL/f'd4_v2_{tag}_runcheck100.jsonl'
                with (LOCAL/f'd4-v2-{tag}.generation.log').open('a') as g:
                    subprocess.run([sys.executable,str(ROOT/'scripts/mac/run_cell.py'),'--cell',f'med_d4_v2_{tag}_runcheck100','--gguf',str(model),'--tokenizer',str(ROOT/'models/merged/med'),'--server-receipt',str(receipt),'--protocol',str(ROOT/'MAC_PREREG.md'),'--split','calib','--inputs',str(ROOT/'models/local-results/day5/runcheck100_prompts.jsonl'),'--stop-eot','--out',str(path)],cwd=ROOT,stdout=g,stderr=subprocess.STDOUT,check=True)
                rows=[json.loads(s) for s in path.read_text().splitlines()];summary=json.loads(path.with_suffix('.summary.json').read_text());spec=json.loads(path.with_suffix('.run.json').read_text())
                if len(rows)!=100 or len({r['prompt_id'] for r in rows})!=100 or {r['prompt_id'] for r in rows}!=set(frozen['prompt_ids']) or spec['input_sha']!=frozen['input_sha'] or not summary['complete'] or summary['errors']:raise ValueError('Operational population or completion mismatch')
                if any(r['stop_token_ids']!=[3,6] or r['control_vector'] is not None for r in rows):raise ValueError('Unexpected operational intervention')
                (OUT/f'd4_v2_{tag}_runcheck100.summary.json').write_text(json.dumps(summary,indent=2)+'\n')
                checks[tag]={'rows':100,'exact_ids_verified':True,'response_sha256':sha256(path),'model_sha256':sha256(model),'stop_token_ids':[3,6],'control_vector':None,'nonreported':True,'zero_final_errors':True}
            finally:
                if receipt.exists():
                    r=json.loads(receipt.read_text());live=subprocess.run(['ps','-p',str(r['pid']),'-o','command='],capture_output=True,text=True).stdout.strip()
                    if live==' '.join(r['command']):os.kill(r['pid'],signal.SIGTERM)
                server.wait(timeout=30)
    result={'corrected_layer0_exclusion':True,'checks':checks,'M18_status':'ready_reuse_v2_medical_Q3_with_same_runtime_vector','M19_status':'reported_protected_random_generation_not_yet_run','steered_full_cells_complete':5,'full_responses':8060,'judgments':'pending_central_D7_for_new_full_cells','random_control_limit':'one seed13 draw; prompt bootstrap excludes tensor-selection variance'}
    (OUT/'corrected_operational_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'completion.json').write_text(json.dumps(result,indent=2)+'\n')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!='manishshaw-nov9':raise RuntimeError('Refusing to publish to another branch')
    paths=['results/mac/nov10','configs/mac/nov9/d4_v2']
    subprocess.run(['git','add','--',*paths],cwd=ROOT,check=True)
    subprocess.run(['git','commit','--only','-m','Complete corrected protection operational checks and M18 reuse readiness','--',*paths],cwd=ROOT,check=True)
    subprocess.run(['git','push','origin','HEAD:manishshaw-nov9'],cwd=ROOT,check=True)
    print('Full steered batch and corrected protection checks complete; all handoffs published',flush=True)


if __name__=='__main__':main()
