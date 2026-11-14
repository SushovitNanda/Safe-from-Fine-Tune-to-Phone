#!/usr/bin/env bash
# Night 3 (7->8 Nov, 02:50-10:00): judge Manish's Mac cells centrally (D7) -> fidelity gate -> ReSta passes until DEADLINE -> select.
#   bash scripts/t2_d7.sh     log: logs/t2_d7.log     (run scripts/import_mac_cells.py first)
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=/c/lexsi/.venv/Scripts/python.exe
SYS_PY="python"
DEADLINE=${DEADLINE:-0920}
MAC=$(ls -d results/cells/mac__* | xargs -n1 basename)
FID=fid50__med__fp16
echo "STEP fid50 laptop generation $(date +%H:%M)"
[ -f results/cells/$FID/records.jsonl ] || { $P harness/run_cell.py --cell $FID --model models/merged/med --weights fp16 --sets fidelity50 > logs/t2_gen_$FID.log 2>&1; echo "exit $?"; }
ARGS=""; for c in $MAC $FID; do ARGS="$ARGS --cell $c"; done
echo "STEP judge qwen3guard $(date +%H:%M)"; $P harness/judge.py $ARGS > logs/t2_judge_mac.log 2>&1; echo "exit $?"
echo "STEP backtranslate_hi $(date +%H:%M)"; IT_DEVICE=cuda IT_MEM_FRACTION=0.6 "$SYS_PY" harness/backtranslate.py $ARGS --langs hi --batch 16 > logs/t2_bt_mac.log 2>&1; echo "exit $?"
echo "STEP wildguard_hi $(date +%H:%M)"; $P harness/judge_wildguard.py $ARGS --langs hi > logs/t2_wildguard_mac.log 2>&1; echo "exit $?"
echo "STEP d7_summary $(date +%H:%M)"; $P harness/d7_summary.py > logs/t2_d7_summary.log 2>&1; echo "exit $?"
MED=models/merged/med
dp () { echo "STEP devpass $1 $(date +%H:%M)"; $P harness/dev_pass.py --name "$@" >> logs/t2_chain_c_devpass.log 2>&1; echo "exit $?"; }
for a in 0.10 0.15 0.20 0.40 0.30; do
  [ -f results/cells/dev_pass__resta_a$a/medmcqa_dev1000.json ] && { echo "skip resta_a$a"; continue; }
  [ "$(date +%H%M)" -ge "$DEADLINE" ] && { echo "DEADLINE $DEADLINE reached, skipping resta_a$a"; continue; }
  dp resta_a$a --model $MED --resta $a
done
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
echo "T2_D7_DONE $(date +%H:%M)"
