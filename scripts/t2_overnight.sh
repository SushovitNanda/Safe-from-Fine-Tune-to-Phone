#!/usr/bin/env bash
# Overnight queue, 10 Nov (one GPU job at a time):
#  1 wait for the five steered GGUF cells to be judged
#  2 back-translation batch-size check on the medical test cell (audit item 12)
#  3 restricted ReSta alpha 0.20 test cell (the best restricted setting on dev, run for completeness)
#  4 until the cutoff: fetch Manish's branch and judge any new ZIP (the RQ6 cells)
# New ZIPs take priority between steps.   bash scripts/t2_overnight.sh   log: logs/t2_overnight.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=/c/lexsi/.venv/Scripts/python.exe
SYS_PY="python"
B=origin/manishshaw-nov9
CUTOFF=${CUTOFF:-0745}

new_zips () {   # copy ZIPs that exist on Manish's branch but not locally; judge them
  git fetch origin manishshaw-nov9 >/dev/null 2>&1
  local n=0
  for f in $(git ls-tree -r --name-only $B | grep -E 'models/local-results/day[0-9]+/.*\.zip$'); do
    if [ ! -f "$f" ]; then mkdir -p "$(dirname "$f")"; git show "$B:$f" > "$f"; echo "new zip $f $(date +%H:%M)"; n=$((n+1)); fi
  done
  if [ "$n" -gt 0 ]; then
    echo "STEP judge_new $(date +%H:%M)"; D7_DATE=2026-11-10 bash scripts/judge_new_zips.sh > logs/t2_judge_new_$(date +%H%M).log 2>&1; echo "exit $?"
  fi
}

while ! grep -q "JUDGE_NEW_ZIPS_DONE" logs/t2_judge_steered.log 2>/dev/null; do
  if ! tasklist | grep -q "bash.exe"; then break; fi; sleep 30
done
echo "steered cells judged $(date +%H:%M)"
new_zips

echo "STEP bt_batch_check $(date +%H:%M)"
C=btcheck16__med__fp16
mkdir -p results/private/$C results/cells/$C
$P -I -c "
import json
with open('results/private/med__fp16__f16__tpl-official/responses.jsonl',encoding='utf-8') as f, open('results/private/$C/responses.jsonl','w',encoding='utf-8') as g:
    for l in f:
        r=json.loads(l)
        if r['lang']=='hi': r['cell']='$C'; g.write(json.dumps(r,ensure_ascii=False)+'\n')
"
IT_DEVICE=cuda IT_MEM_FRACTION=0.6 "$SYS_PY" harness/backtranslate.py --cell $C --langs hi --batch 16 > logs/t2_btcheck_bt.log 2>&1; echo "exit $?"
$P harness/judge_wildguard.py --cell $C --langs hi > logs/t2_btcheck_wg.log 2>&1; echo "exit $?"
$P scripts/bt_batch_check.py > logs/t2_btcheck_compare.log 2>&1; echo "compare exit $?"
[ -f results/judges/backtranslation_$C.jsonl ] && mv results/judges/backtranslation_$C.jsonl results/private/$C/
new_zips

if [ "$(date +%H%M)" -lt 0640 ]; then
  c=cresta-a0.20-top20__fp16__f16__tpl-official
  TEST="aya_en_test aya_hi_test aya_hinglish_test clinicsafe_hi_en clinicsafe_hi_hi clinicsafe_hi_hinglish xstest_en_test xstest_hi_test xstest_hinglish_test"
  O="--resta 0.20 --resta_tensors locate/cresta_tensors_v2_top20.json"
  echo "STEP gen $c $(date +%H:%M)"; $P harness/run_cell.py --cell $c --model models/merged/med --weights fp16 --sets $TEST $O > logs/t2_gen_$c.log 2>&1; echo "exit $?"
  echo "STEP medmcqa $c $(date +%H:%M)"; $P scripts/eval/medmcqa_score.py --model models/merged/med --set Datasets/final/medmcqa_test_500/prompts.jsonl --out results/cells/$c/medmcqa_test500.json $O > logs/t2_mq_$c.log 2>&1; echo "exit $?"
  echo "STEP judge $c $(date +%H:%M)"; $P harness/judge.py --cell $c > logs/t2_judge_$c.log 2>&1; echo "exit $?"
  IT_DEVICE=cuda "$SYS_PY" harness/backtranslate.py --cell $c --langs hi > logs/t2_bt_$c.log 2>&1; echo "exit $?"
  $P harness/judge_wildguard.py --cell $c --langs hi > logs/t2_wg_$c.log 2>&1; echo "exit $?"
  echo "CELL_DONE $c $(date +%H:%M)"
else
  echo "cresta a0.20 test cell skipped: past 06:40"
fi

while [ "$(date +%H%M)" -lt "$CUTOFF" ]; do new_zips; sleep 120; done
echo "T2_OVERNIGHT_DONE $(date +%H:%M)"
