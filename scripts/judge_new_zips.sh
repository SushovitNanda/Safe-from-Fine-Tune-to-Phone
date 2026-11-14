#!/usr/bin/env bash
# Judge Manish's newly delivered Mac ZIPs (models/local-results/day*/*.zip) centrally: import, then for every mac__* cell lacking
# complete labels run Qwen3Guard -> back-translation (Hindi) -> WildGuard (Hindi), then deliver a text-free D7 summary of the cells
# not yet in any handoff/D7_*/ folder. Safe to re-run: the import leaves unchanged cells alone and refuses to change judged ones,
# every judge resumes, and with nothing new the GPU is not touched and no delivery is written. Exits non-zero on any failed step.
#
#   bash scripts/judge_new_zips.sh                     log: logs/judge_new_zips_<stamp>_<step>.log
#   D7_DATE=2026-11-10 ...                             delivery date (default today); handoff/D7_<date>/, suffix _2, _3.. if taken
#   FID_MAP="mac__x_fidelity50=fid50__y__fp16 ..."     fidelity pairs when the name rule (mac__<x>_f16_fidelity50 -> fid50__<x>__fp16) misses
#   D7_DEST=<dir> DELIVER_ALL=1                        test only: write the summary to <dir>; include already delivered cells
#
# After a fidelity-only ZIP, read the PASS/FAIL line in the summary log; the gate result does not change this script's exit code.
set -uo pipefail
cd . || exit 1
export PYTHONUTF8=1 HF_HUB_OFFLINE=1 HF_HOME="models/hf_cache" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
P=/c/lexsi/.venv/Scripts/python.exe
SYS_PY="python"
STAMP=$(date +%Y%m%d_%H%M%S)
L=logs/judge_new_zips_$STAMP

fail() { echo "FAILED: $*" >&2; exit 1; }
step() { # step <name> <command...>; output to the step log; stop on non-zero
  local name=$1; shift
  echo "STEP $name $(date +%H:%M:%S)"
  "$@" > "${L}_$name.log" 2>&1 || fail "$name exit $? (see ${L}_$name.log)"
}

state() { # state <qwen|bt|wg|incomplete|deliver|all|table>: cell names (one per line), or a text-free table for 'table'
  "$P" - "$1" <<'PY' | tr -d '\015'
import glob, json, os, sys
from pathlib import Path
mode = sys.argv[1]
def rj(p):
    with open(p, encoding="utf-8") as f: return [json.loads(l) for l in f if l.strip()]
def ids(p): return {r["prompt_id"] for r in rj(p)} if os.path.exists(p) else set()
out = []
for d in sorted(glob.glob("results/cells/mac__*")):
    c = os.path.basename(d)
    rows = rj(f"results/private/{c}/responses.jsonl")
    all_ids = {r["prompt_id"] for r in rows}; hi = {r["prompt_id"] for r in rows if r["lang"] == "hi"}
    q, w, b = ids(f"{d}/labels_qwen3guard.jsonl"), ids(f"{d}/labels_wildguard.jsonl"), ids(f"results/judges/backtranslation_{c}.jsonl")
    need = {"qwen": q != all_ids, "bt": not hi <= b, "wg": w != hi}
    delivered = any(os.path.exists(f"{h}/{c}/labels_qwen3guard.jsonl") for h in glob.glob("handoff/D7_*"))
    if mode in need:
        if need[mode]: print(c)
    elif mode == "incomplete":
        if any(need.values()): print(c)
    elif mode == "deliver":
        if not any(need.values()) and not delivered: print(c)
    elif mode == "all":
        if not any(need.values()): print(c)
    elif mode == "table":
        labs = rj(f"{d}/labels_qwen3guard.jsonl") if os.path.exists(f"{d}/labels_qwen3guard.jsonl") else []
        wg = rj(f"{d}/labels_wildguard.jsonl") if os.path.exists(f"{d}/labels_wildguard.jsonl") else []
        unsure = sum(1 for r in labs if "unsure" in (r["safety"], r["refusal"])) + sum(1 for r in wg if r["harmful_response"] == "unsure")
        out.append(f"{c}: answers {len(all_ids)} qwen3guard {len(q & all_ids)} hindi {len(hi)} backtranslated {len(hi & b)} wildguard {len(hi & w)} unsure {unsure} delivered {'yes' if delivered else 'no'}")
print("\n".join(out), end="\n" if out else "")
PY
}

step import "$P" scripts/import_mac_cells.py

Q=$(state qwen) || fail "state qwen"
B=$(state bt) || fail "state bt"
W=$(state wg) || fail "state wg"
cell_args() { local a=""; for c in $1; do a="$a --cell $c"; done; echo "$a"; }

if [ -n "$Q$B$W" ]; then echo "to judge: qwen3guard [$(echo $Q)] backtranslate [$(echo $B)] wildguard [$(echo $W)]"; else echo "nothing to judge"; fi

# Each step is a separate process, so the GPU holds one model at a time.
if [ -n "$Q" ]; then step qwen3guard "$P" harness/judge.py $(cell_args "$Q"); fi
if [ -n "$B" ]; then step backtranslate env IT_DEVICE=cuda IT_MEM_FRACTION=0.6 "$SYS_PY" harness/backtranslate.py $(cell_args "$B") --langs hi --batch 16; fi
# Back-translation runs first, so a cell new to it also needs WildGuard; recompute after the steps above.
W=$(state wg) || fail "state wg"
if [ -n "$W" ]; then step wildguard "$P" harness/judge_wildguard.py $(cell_args "$W") --langs hi; fi

R=$(state incomplete) || fail "state incomplete"
[ -z "$R" ] || fail "still incomplete after judging: $(echo $R)"

if [ "${DELIVER_ALL:-0}" = 1 ]; then CELLS=$(state all) || fail "state all"; else CELLS=$(state deliver) || fail "state deliver"; fi
if [ -z "$CELLS" ]; then
  echo "no new cells to deliver; no D7 folder written"
else
  ARGS=""
  for pair in ${FID_MAP:-}; do ARGS="$ARGS --fid $pair"; done
  if [ -n "${D7_DEST:-}" ]; then
    ARGS="$ARGS --dest $D7_DEST"
  else
    BASE=${D7_DATE:-$(date +%F)}; TAG=$BASE; i=1
    while [ -e "handoff/D7_$TAG" ]; do i=$((i+1)); TAG=${BASE}_$i; done
    ARGS="$ARGS --date $TAG"
  fi
  echo "delivering: $(echo $CELLS)"
  step d7_summary "$P" harness/d7_summary.py --cells $CELLS $ARGS
  tail -n 4 "${L}_d7_summary.log" | cut -c1-500
fi

echo "cell status:"
state table || fail "state table"
echo "JUDGE_NEW_ZIPS_DONE $(date +%H:%M:%S)"
