#!/usr/bin/env bash
# Chain E (night of 8-9 Nov): repair TEST cells, all fixed before generation by PREREG amendment 3.
# Step 0 re-generates the medical dev cell under amendment 2 and compares it with the frozen cell (same batches).
# Primary cells first (ReSta alpha 0.05 and steering L24 s0.5, FP16 and NF4), then the secondary cells while time allows.
#   bash scripts/t2_chain_e.sh    log: logs/t2_chain_e.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=python
SYS_PY="python"
DEADLINE=${DEADLINE:-0720}      # no new test cell started at/after this HHMM (a cell takes up to ~65 min, tables follow)
TEST="aya_en_test aya_hi_test aya_hinglish_test clinicsafe_hi_en clinicsafe_hi_hi clinicsafe_hi_hinglish xstest_en_test xstest_hi_test xstest_hinglish_test"
MQT=Datasets/final/medmcqa_test_500/prompts.jsonl
MED=models/merged/med
STEER="--steer models/steer/med_trilingual.pt --steer_layer 24"
before_deadline () { [ "$(date +%H%M)" -lt "$DEADLINE" ]; }

echo "STEP amend2_check $(date +%H:%M)"
CK=results/private/amend2_check
$P harness/run_cell.py --cell amend2_med --model $MED --weights fp16 --ids Datasets/final/dev_pass_ids.jsonl --out $CK > logs/t2_amend2_gen.log 2>&1; echo "exit $?"
$P scripts/amend2_compare.py > logs/t2_amend2_compare.log 2>&1; echo "compare exit $?"

cell () {  # cell-name model weights [extra run_cell/medmcqa options]
  local c=$1 m=$2 w=$3; shift 3
  local flag=""; [ "$w" = nf4 ] && flag="--nf4"
  [ -f results/cells/$c/labels_wildguard.jsonl ] && { echo "skip $c"; return; }
  before_deadline || { echo "DEADLINE $DEADLINE reached, skipping $c"; return; }
  echo "STEP gen $c $(date +%H:%M)"
  $P harness/run_cell.py --cell $c --model $m --weights $w --sets $TEST "$@" > logs/t2_gen_$c.log 2>&1; echo "exit $?"
  if [ ! -f results/cells/$c/medmcqa_test500.json ]; then
    echo "STEP medmcqa $c $(date +%H:%M)"
    $P scripts/eval/medmcqa_score.py --model $m --set $MQT --out results/cells/$c/medmcqa_test500.json $flag "$@" > logs/t2_mq_$c.log 2>&1; echo "exit $?"
  fi
  echo "STEP judge $c $(date +%H:%M)"
  $P harness/judge.py --cell $c > logs/t2_judge_$c.log 2>&1; echo "exit $?"
  echo "STEP bt+wildguard $c $(date +%H:%M)"
  IT_DEVICE=cuda "$SYS_PY" harness/backtranslate.py --cell $c --langs hi > logs/t2_bt_$c.log 2>&1; echo "exit $?"
  $P harness/judge_wildguard.py --cell $c --langs hi > logs/t2_wg_$c.log 2>&1; echo "exit $?"
  echo "CELL_DONE $c $(date +%H:%M)"
}

# primary
cell rep-resta-a0.05__fp16__f16__tpl-official models/merged/rep-resta-a0.05 fp16
cell rep-resta-a0.05__nf4__f16__tpl-official  models/merged/rep-resta-a0.05 nf4
cell steer-L24-s0.5__fp16__f16__tpl-official  $MED fp16 $STEER --steer_strength 0.5
cell steer-L24-s0.5__nf4__f16__tpl-official   $MED nf4  $STEER --steer_strength 0.5
# secondary (PREREG section 8 fallback points and the in-grid ReSta)
cell steer-L24-s1.0__fp16__f16__tpl-official  $MED fp16 $STEER --steer_strength 1.0
cell resta-a0.20__fp16__f16__tpl-official     $MED fp16 --resta 0.20
cell cresta-a0.25-top20__fp16__f16__tpl-official $MED fp16 --resta 0.25 --resta_tensors locate/cresta_tensors_v2_top20.json
cell rep-resta-a0.10__fp16__f16__tpl-official models/merged/rep-resta-a0.10 fp16

if [ -f harness/rq4_tables.py ]; then
  echo "STEP rq4_tables $(date +%H:%M)"; $P harness/rq4_tables.py --out results/repair_test > logs/t2_rq4_tables.log 2>&1; echo "exit $?"
fi
echo "T2_CHAIN_E_DONE $(date +%H:%M)"
