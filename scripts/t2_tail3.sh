#!/usr/bin/env bash
# Night-2 tail 3: after t2_tail2.sh (Hindi half-run rerun + tables) -> validation with the preamble (3 languages, fixed
# loader) -> tables with floors -> ReSta dev passes until DEADLINE -> select.
#   bash scripts/t2_tail3.sh      log: logs/t2_tail3.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CIRCUITKIT_SKIP_MEM_GUARD=1
P=/c/lexsi/.venv/Scripts/python.exe
DEADLINE=${DEADLINE:-0830}
while ! grep -q "T2_TAIL2_DONE" logs/t2_tail2.log 2>/dev/null; do sleep 30; done
echo "tail2 done $(date +%H:%M)"
for lang in en hi hinglish; do
  [ -f results/circuits/v2/validation_$lang.json ] && { echo "skip validate $lang"; continue; }
  echo "STEP validate $lang $(date +%H:%M)"; $P locate/validate_circuit.py --lang $lang > logs/t2_validate_$lang.log 2>&1; echo "exit $?"
done
echo "STEP tables $(date +%H:%M)"; $P locate/tensor_map_v2.py > logs/t2_tensor_map_v2.log 2>&1; echo "exit $?"
MED=models/merged/med
dp () { echo "STEP devpass $1 $(date +%H:%M)"; $P harness/dev_pass.py --name "$@" >> logs/t2_chain_c_devpass.log 2>&1; echo "exit $?"; }
for a in 0.25 0.15 0.40 0.10 0.20 0.30; do
  [ "$(date +%H%M)" -ge "$DEADLINE" ] && { echo "DEADLINE $DEADLINE reached, skipping resta_a$a"; continue; }
  dp resta_a$a --model $MED --resta $a
done
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
echo "T2_TAIL3_DONE $(date +%H:%M)"
