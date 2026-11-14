#!/usr/bin/env bash
# Restricted ReSta at the points PREREG section 8 named but chain C skipped: best in-grid alpha by dev ASR (0.20) and +/- 0.1, top-20 % list.
# Dev only; runs after the rep-resta-a0.10 test cell. Found missing by the independent audit of 9 Nov.
#   bash scripts/t2_cresta_prereg.sh    log: logs/t2_cresta_prereg.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=/c/lexsi/.venv/Scripts/python.exe
DEADLINE=${DEADLINE:-2155}
while ! grep -q "T2_CHAIN_E_DONE" logs/t2_chain_e2.log 2>/dev/null; do sleep 20; done
for a in 0.20 0.10 0.30; do
  [ "$(date +%H%M)" -ge "$DEADLINE" ] && { echo "DEADLINE $DEADLINE reached, skipping cresta_a${a}_top20"; continue; }
  echo "STEP devpass cresta_a${a}_top20 $(date +%H:%M)"
  $P harness/dev_pass.py --name cresta_a${a}_top20 --model models/merged/med --resta $a --resta_tensors locate/cresta_tensors_v2_top20.json >> logs/t2_cresta_prereg_devpass.log 2>&1; echo "exit $? $(date +%H:%M)"
done
$P harness/select.py > logs/t2_select.log 2>&1; echo "select exit $?"
$P harness/select_variants.py > logs/t2_select_variants.log 2>&1; echo "variants exit $?"
echo "T2_CRESTA_PREREG_DONE $(date +%H:%M)"
