#!/usr/bin/env bash
# Chain D (8 Nov evening, user away 2 h): steering strength screen on the two best layers from chain C (24, 27) at
# strengths 0.5 / 0.75 / 0.25 (most informative first), each a full dev pass (360 ids + MedMCQA dev-995, Hindi
# back-translation + WildGuard). First cells generated under PREREG amendment 2 (stop on END_OF_TURN 6 as well as EOS 3).
#   bash scripts/t2_chain_d.sh    log: logs/t2_chain_d.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=python
DEADLINE=${DEADLINE:-2150}      # no new dev pass started at/after this HHMM
MED=models/merged/med
STEER=models/steer/med_trilingual.pt
dp () { echo "STEP devpass $1 $(date +%H:%M)"; $P harness/dev_pass.py --name "$@" >> logs/t2_chain_d_devpass.log 2>&1; echo "exit $? $(date +%H:%M)"; }
before_deadline () { [ "$(date +%H%M)" -lt "$DEADLINE" ]; }
for LS in 24:0.5 27:0.5 24:0.75 27:0.75 24:0.25 27:0.25; do
  L=${LS%%:*}; S=${LS##*:}
  [ -f results/cells/dev_pass__steer_L${L}_s$S/medmcqa_dev1000.json ] && { echo "skip steer L$L s$S"; continue; }
  before_deadline || { echo "DEADLINE $DEADLINE reached, skipping steer L$L s$S"; continue; }
  dp steer_L${L}_s$S --model $MED --steer $STEER --steer_layer $L --steer_strength $S
done
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
$P harness/select_variants.py > logs/t2_select_variants.log 2>&1; echo "variants exit $?"
echo "T2_CHAIN_D_DONE $(date +%H:%M)"
