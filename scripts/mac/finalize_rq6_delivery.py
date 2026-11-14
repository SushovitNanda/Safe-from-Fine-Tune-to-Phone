"""Verify the completed M19 pair, record accurate remaining dependencies and push status.

No local judging, public release or inferred safety result is performed.
"""
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]


def main():
    local=ROOT/'models/local-results/day8';out=ROOT/'results/mac/nov11'
    while True:
        s=json.loads((local/'SESSION_STATE.json').read_text())
        if s['status']=='failed':raise RuntimeError('M19 pipeline failed; resolve its recorded error')
        if s['status']=='complete':
            c=subprocess.run(['ps','-p',str(s['pid']),'-o','command='],text=True,capture_output=True).stdout
            if 'run_rq6_cells.py' not in c:break
        time.sleep(30)
    cells=['rep_steer_q3km-protected','rep_steer_q3km-random']
    if set(s['completed_cells'])!=set(cells) or s.get('completed_responses')!=3224:raise ValueError('Both M19 cells must be complete')
    import sys
    sys.path.insert(0,str(ROOT/'scripts/mac'))
    from run_rq6_cells import validate_cell
    expected=set(json.loads((ROOT/'configs/mac/nov5_inputs.json').read_text())['test_prompt_ids'])
    for cell in cells:validate_cell(cell,expected)
    s['external_blockers']=['New central D7 labels for BOTH M19 cells; final RQ6 tables then refresh','Public release is a separate action after the team go-ahead']
    for p in [local/'SESSION_STATE.json',out/'status.json']:p.write_text(json.dumps(s,indent=2)+'\n')
    result={'M19_generation':'complete','full_cells':2,'validated_responses':3224,'both_archives':{c:s['completed_cells'][c]['archive'] for c in cells},'D2_numeric_comparison':'resolved','RQ5_D8':'prepared_and_centrally_labelled','RQ6_D8':'awaiting_new_central_labels','public_release':'prepared_not_performed'}
    (out/'m19_completion.json').write_text(json.dumps(result,indent=2)+'\n')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!='manishshaw-nov9':raise RuntimeError('Refusing to publish to another branch')
    subprocess.run(['git','add','--','results/mac/nov11'],cwd=ROOT,check=True)
    subprocess.run(['git','commit','--only','-m','Verify complete M19 pair and record remaining central-judging dependency','--','results/mac/nov11'],cwd=ROOT,check=True)
    subprocess.run(['git','push','origin','HEAD:manishshaw-nov9'],cwd=ROOT,check=True)
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
