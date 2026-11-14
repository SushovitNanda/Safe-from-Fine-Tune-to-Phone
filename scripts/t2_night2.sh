#!/usr/bin/env bash
# Night 2 (5→6 Nov): light → heavy, each step gated on free VRAM (the user runs another GPU process early in the night).
#   1. Hindi back-translation on the GPU (IndicTrans2 FP16, ~3 GB)            needs 3.5 GB free
#   2. WildGuard 8-bit on the Hindi answers (~7.5 GB) + tables + baseline rows  needs 8.5 GB free
#   3. chain B stage 2 (12 split-half runs + validation; peaks 17 GB)          needs 10.5 GB free (GPU otherwise idle)
#   4. chain C ReSta alpha dev passes until the deadline, then select.py       same gate; stops starting passes at DEADLINE
#   bash scripts/t2_night2.sh      log: logs/t2_night2.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CIRCUITKIT_SKIP_MEM_GUARD=1
P=python
SYS_PY="python"
DEADLINE=${DEADLINE:-0830}
TOTAL=12282
wait_gpu () {  # $1 = MiB that must be free (between our own steps, memory.used is other people's processes + desktop)
  while :; do
    used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' '); free=$((TOTAL - used))
    [ "$free" -ge "$1" ] && { echo "GPU free ${free}MiB >= ${1}MiB $(date +%H:%M)"; return; }
    echo "WAIT gpu used=${used}MiB, need ${1}MiB free $(date +%H:%M)"; sleep 120
  done
}
CELLS="orig__fp16__f16__tpl-official med__fp16__f16__tpl-official ctrl__fp16__f16__tpl-official orig__nf4__f16__tpl-official med__nf4__f16__tpl-official dev_pass__orig__fp16 dev_pass__med__fp16 dev_pass__ctrl__fp16"
ARGS=""; for c in $CELLS; do ARGS="$ARGS --cell $c"; done

# 1. back-translation (light)
wait_gpu 3500
echo "STEP backtranslate_hi $(date +%H:%M)"; IT_DEVICE=cuda IT_MEM_FRACTION=${IT_MEM_FRACTION:-0.40} "$SYS_PY" harness/backtranslate.py $ARGS --langs hi --batch ${BT_BATCH:-8} > logs/t2_bt_hi.log 2>&1; echo "exit $?"

# 2. WildGuard (medium) + tables + baseline rows
wait_gpu 8500
echo "STEP wildguard_hi $(date +%H:%M)"; $P harness/judge_wildguard.py $ARGS --langs hi > logs/t2_wildguard_hi.log 2>&1; echo "exit $?"
echo "STEP rq_tables $(date +%H:%M)"; $P harness/rq_tables.py --out results/drift > logs/t2_rq_tables.log 2>&1; echo "exit $?"
echo "STEP rq_tables_qwen3guard $(date +%H:%M)"; $P harness/rq_tables.py --out results/drift_qwen3guard --primary qwen3guard > logs/t2_rq_tables_qwen3guard.log 2>&1; echo "exit $?"
echo "STEP dev_baseline_rows $(date +%H:%M)"
for m in orig med ctrl; do $P harness/dev_pass.py --name baseline_$m --model models/merged/$m --cell dev_pass__${m}__fp16 --sweep results/repair_dev/baselines_v2.jsonl >> logs/t2_dev_baseline_rows.log 2>&1; echo "exit $?"; done

# 3. chain B stage 2 (heavy)
wait_gpu 10500
echo "STEP chain_b_stage2 $(date +%H:%M)"; bash scripts/t2_chain_b.sh stage2 > logs/t2_chain_b2.log 2>&1; echo "exit $?"

# 4. chain C ReSta sweep until the deadline (each dev pass resumable; ~25 min)
MED=models/merged/med
dp () { echo "STEP devpass $1 $(date +%H:%M)"; $P harness/dev_pass.py --name "$@" >> logs/t2_chain_c_devpass.log 2>&1; echo "exit $?"; }
for a in 0.25 0.15 0.40 0.10 0.20 0.30; do
  [ "$(date +%H%M)" -ge "$DEADLINE" ] && { echo "DEADLINE $DEADLINE reached, skipping resta_a$a"; continue; }
  wait_gpu 10500; dp resta_a$a --model $MED --resta $a
done
echo "STEP select $(date +%H:%M)"; $P harness/select.py > logs/t2_select.log 2>&1; echo "exit $?"
echo "T2_NIGHT2_DONE $(date +%H:%M)"
