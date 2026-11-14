#!/usr/bin/env bash
# Night-3 tail (8 Nov): after t2_d7.sh -> circuit-restricted ReSta (alpha 0.25 x top5/10/20) -> steering calibration ->
# layer screen until DEADLINE -> select.  Weight-space repairs first: D5 to Manish must be ReSta or cresta (steering cannot ship in a GGUF).
#   bash scripts/t2_tail4.sh    log: logs/t2_tail4.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=python
DEADLINE=${DEADLINE:-0920}
MED=models/merged/med
while ! grep -q "T2_D7_DONE" logs/t2_d7.log 2>/dev/null; do sleep 30; done
echo "d7 queue done $(date +%H:%M)"
dp () { echo "STEP devpass $1 $(date +%H:%M)"; $P harness/dev_pass.py --name "$@" >> logs/t2_chain_c_devpass.log 2>&1; echo "exit $?"; }
before_deadline () { [ "$(date +%H%M)" -lt "$DEADLINE" ]; }
for pct in 5 10 20; do
  [ -f results/cells/dev_pass__cresta_a0.25_top$pct/medmcqa_dev1000.json ] && { echo "skip cresta top$pct"; continue; }
  before_deadline || { echo "DEADLINE $DEADLINE reached, skipping cresta top$pct"; continue; }
  dp cresta_a0.25_top$pct --model $MED --resta 0.25 --resta_tensors locate/cresta_tensors_v2_top$pct.json
done
if before_deadline && [ ! -f results/cells/dev_pass__resta_a0.05/medmcqa_dev1000.json ]; then
  dp resta_a0.05 --model $MED --resta 0.05      # dev-only extra point below the pre-registered grid (logged as exploratory)
fi
if [ ! -f models/steer/med_trilingual.pt ] && before_deadline; then
  echo "STEP steer_calibrate $(date +%H:%M)"; $P repair/steer_calibrate.py --model $MED --pairs trilingual --out models/steer/med_trilingual.pt > logs/t2_steer_calibrate.log 2>&1; echo "exit $?"
fi
STRENGTH=${STEER_STRENGTH:-1.0}
for L in 27 33 24 30; do
  [ -f models/steer/med_trilingual.pt ] || break
  [ -f results/cells/dev_pass__steer_L${L}_s$STRENGTH/medmcqa_dev1000.json ] && { echo "skip steer L$L"; continue; }
  before_deadline || { echo "DEADLINE $DEADLINE reached, skipping steer L$L"; continue; }
  dp steer_L${L}_s$STRENGTH --model $MED --steer models/steer/med_trilingual.pt --steer_layer $L --steer_strength $STRENGTH
done
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
echo "T2_TAIL4_DONE $(date +%H:%M)"
