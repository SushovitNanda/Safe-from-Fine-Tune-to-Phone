#!/usr/bin/env bash
# Night-3 tail 5: after t2_tail4.sh, exploratory circuit-restricted ReSta at larger alpha on the top-20 % list (dev only;
# outside the pre-registered grid, logged as exploratory) while the GPU is still free before the user's 10:00 deadline.
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=/c/lexsi/.venv/Scripts/python.exe
DEADLINE=${DEADLINE:-0945}
while ! grep -q "T2_TAIL4_DONE" logs/t2_tail4.log 2>/dev/null; do sleep 30; done
dp () { echo "STEP devpass $1 $(date +%H:%M)"; $P harness/dev_pass.py --name "$@" >> logs/t2_chain_c_devpass.log 2>&1; echo "exit $?"; }
for a in 0.5 1.0; do
  [ "$(date +%H%M)" -ge "$DEADLINE" ] && { echo "DEADLINE $DEADLINE reached, skipping cresta_a${a}_top20"; continue; }
  dp cresta_a${a}_top20 --model models/merged/med --resta $a --resta_tensors locate/cresta_tensors_v2_top20.json
done
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
echo "T2_TAIL5_DONE $(date +%H:%M)"
