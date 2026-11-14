#!/usr/bin/env bash
# 10 Nov evening queue (one GPU job at a time): finish the back-translation batch check (resumable), then the restricted ReSta
# alpha 0.20 test cell.   bash scripts/t2_eve.sh   log: logs/t2_eve.log
cd .
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=python
SYS_PY="python"
C=btcheck16__med__fp16
echo "STEP bt_batch_check $(date +%H:%M)"
IT_DEVICE=cuda IT_MEM_FRACTION=0.6 "$SYS_PY" harness/backtranslate.py --cell $C --langs hi --batch 16 >> logs/t2_btcheck_bt.log 2>&1; echo "exit $?"
$P harness/judge_wildguard.py --cell $C --langs hi >> logs/t2_btcheck_wg.log 2>&1; echo "exit $?"
$P scripts/bt_batch_check.py > logs/t2_btcheck_compare.log 2>&1; echo "compare exit $?"
[ -f results/judges/backtranslation_$C.jsonl ] && mv results/judges/backtranslation_$C.jsonl results/private/$C/
c=cresta-a0.20-top20__fp16__f16__tpl-official
TEST="aya_en_test aya_hi_test aya_hinglish_test clinicsafe_hi_en clinicsafe_hi_hi clinicsafe_hi_hinglish xstest_en_test xstest_hi_test xstest_hinglish_test"
O="--resta 0.20 --resta_tensors locate/cresta_tensors_v2_top20.json"
echo "STEP gen $c $(date +%H:%M)"; $P harness/run_cell.py --cell $c --model models/merged/med --weights fp16 --sets $TEST $O > logs/t2_gen_$c.log 2>&1; echo "exit $?"
echo "STEP medmcqa $c $(date +%H:%M)"; $P scripts/eval/medmcqa_score.py --model models/merged/med --set Datasets/final/medmcqa_test_500/prompts.jsonl --out results/cells/$c/medmcqa_test500.json $O > logs/t2_mq_$c.log 2>&1; echo "exit $?"
echo "STEP judge $c $(date +%H:%M)"; $P harness/judge.py --cell $c > logs/t2_judge_$c.log 2>&1; echo "exit $?"
IT_DEVICE=cuda "$SYS_PY" harness/backtranslate.py --cell $c --langs hi > logs/t2_bt_$c.log 2>&1; echo "exit $?"
$P harness/judge_wildguard.py --cell $c --langs hi > logs/t2_wg_$c.log 2>&1; echo "exit $?"
$P harness/final_stats.py > logs/t2_final_stats.log 2>&1; echo "final_stats exit $?"
echo "T2_EVE_DONE $(date +%H:%M)"
