#!/usr/bin/env bash
# Night-2 tail (replaces the ReSta phase of t2_night2.sh): redo the split-half run that hit a transient CUDA OOM
# (med/hi/half-a, 04:34), rebuild the v2 tables with floors, then one ReSta dev pass if before DEADLINE, then select.
#   bash scripts/t2_tail2.sh      log: logs/t2_tail2.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CIRCUITKIT_SKIP_MEM_GUARD=1
P=python
DEADLINE=${DEADLINE:-0830}
for i in 1 2; do
  [ -f results/circuits/v2/med_hi_half-a_eap-ig_scores.json ] && break
  sleep 20
  echo "STEP ck med hi a (retry $i) $(date +%H:%M)"; $P locate/run_circuitkit_v2.py --tag med --model models/merged/med --lang hi --half a > logs/t2_ck_med_hi_half-a_retry$i.log 2>&1; echo "exit $?"
done
echo "STEP tables $(date +%H:%M)"; $P locate/tensor_map_v2.py > logs/t2_tensor_map_v2.log 2>&1; echo "exit $?"
if [ "$(date +%H%M)" -lt "$DEADLINE" ]; then
  echo "STEP devpass resta_a0.25 $(date +%H:%M)"; $P harness/dev_pass.py --name resta_a0.25 --model models/merged/med --resta 0.25 >> logs/t2_chain_c_devpass.log 2>&1; echo "exit $?"
else
  echo "DEADLINE $DEADLINE reached, no ReSta pass"
fi
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
echo "T2_TAIL2_DONE $(date +%H:%M)"
