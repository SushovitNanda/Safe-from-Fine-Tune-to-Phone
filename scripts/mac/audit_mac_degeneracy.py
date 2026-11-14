"""Reproduce central heuristic sensitivity from local raw outputs; emit text-free counts."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import zlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'harness'))
from stats import load_labels,unsafe,HARM


def main():
    source=(ROOT/'scripts/mac_degeneracy.py').read_text();tree=ast.parse(source)
    funcs='\n\n'.join(ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['tok','degenerate'])
    ns={'re':re,'Counter':Counter,'zlib':zlib};exec(compile(funcs,'central_degeneracy_functions','exec'),ns);detect=ns['degenerate'];out={}
    cells=['med_f16','med_q4km','med_q3km','med_q4km-nopre','med_budget-phone','rep_steer_f16','rep_steer_q4km','rep_steer_q3km','rep_steer_q4km-nopre','rep_steer_budget-phone','orig_q4km','orig_q4km-nopre','rep_steer_q3km-protected','rep_steer_q3km-random']
    for c in cells:
        folder='day8' if c.endswith(('-protected','-random')) else 'day7' if c.startswith('rep_steer') else 'day3' if c.startswith('med_') else 'day2'
        path=ROOT/f'models/local-results/{folder}/{c}.jsonl';rows={r['prompt_id']:r for r in (json.loads(x) for x in path.read_text().splitlines())};labels=load_labels('mac__'+c)
        if set(rows)!=set(labels):raise ValueError('Raw/label coverage mismatch')
        stats={}
        for lang in ['all','en','hi','hinglish']:
            ids=[i for i,r in labels.items() if r['set'] in HARM and (lang=='all' or r['lang']==lang)];flags={i:detect(rows[i]['text'],rows[i]['response']) for i in ids};keep=[i for i in ids if flags[i] is None]
            stats[lang]={'n':len(ids),'flag_counts':dict(Counter(v for v in flags.values() if v)), 'degenerate_pct':round(100*(len(ids)-len(keep))/len(ids),1),'primary_ASR_pct':100*sum(unsafe(labels[i]) for i in ids)/len(ids),'non_degenerate_n':len(keep),'non_degenerate_ASR_pct':100*sum(unsafe(labels[i]) for i in keep)/len(keep) if keep else None}
        out[c]=stats
    result={'cells':out,'heuristic_function_sha256':hashlib.sha256(funcs.encode()).hexdigest(),'scope':'Post-hoc heuristic sensitivity, not an alternative primary analysis or human quality adjudication. Includes too_short flags which can capture legitimate short refusals. No raw completions are written.','central_primary_counts_preserved':True}
    (ROOT/'results/mac/nov11/degeneracy_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('MedicalF16 degeneracy:',out['med_f16']['all']['degenerate_pct'],out['med_f16']['hinglish']['degenerate_pct'])


if __name__=='__main__':main()
