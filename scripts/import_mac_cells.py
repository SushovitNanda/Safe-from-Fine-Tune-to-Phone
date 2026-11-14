"""Import Manish's Mac GGUF cells (D6 ZIPs under models/local-results/day*/) into the laptop harness layout so they can be
judged centrally (plan v3: one judge, one machine).

    python scripts/import_mac_cells.py            -> results/private/mac__<cell>/responses.jsonl  (prompt + answer; git-ignored)
                                                     results/cells/mac__<cell>/records.jsonl     (text-free)
                                                     Datasets/final/fidelity50/prompts.jsonl     (the agreed 50-prompt fidelity set)
Mac rows: 'text' = prompt, 'response' = answer (README in the ZIP). Prompt metadata (set_name) is joined by prompt_id from
Datasets/final/*/prompts.jsonl; calibration ids (fidelity set) get set_name 'fidelity50'. Idempotent: a cell whose content is
unchanged is left untouched (files and timestamps). A ZIP that would change the content of a cell that already has labels or a
back-translation stops the import with an error and writes nothing, so labels can never silently refer to different answers.
"""
import glob, hashlib, json, os, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))
from prompts import index

idx = index()
out_cells = {}
fid_prompts = None
for z in sorted(glob.glob(str(ROOT / "models" / "local-results" / "day*" / "*.zip"))):
    zf = zipfile.ZipFile(z)
    for name in zf.namelist():
        if not name.endswith(".jsonl"): continue
        rows = [json.loads(l) for l in zf.read(name).decode("utf-8").splitlines() if l.strip()]
        if not rows: continue
        if name.endswith("fidelity50_prompts.jsonl"):
            fid_prompts = rows; continue
        if "response" not in rows[0] or "prompt_id" not in rows[0]: continue
        cell_id = rows[0]["cell_id"]
        assert {r["cell_id"] for r in rows} == {cell_id}, f"{os.path.basename(z)}:{name}: more than one cell_id in one file"
        assert len({r["prompt_id"] for r in rows}) == len(rows), f"{os.path.basename(z)}:{name}: duplicate prompt_ids"
        cell = f"mac__{cell_id}"
        assert cell not in out_cells, f"{cell} appears in two ZIPs ({out_cells[cell]['zip']}, {os.path.basename(z)}); keep one"
        out_cells[cell] = {"zip": os.path.basename(z), "zip_path": z, "member": name, "rows": rows}
        print(f"{cell}: {len(rows)} rows from {os.path.basename(z)}:{name}")

assert fid_prompts, "fidelity50_prompts.jsonl not found in the day2 ZIP"
fd = ROOT / "Datasets" / "final" / "fidelity50"; fd.mkdir(parents=True, exist_ok=True)
fid_path = fd / "prompts.jsonl"
if fid_path.exists():
    have = {json.loads(l)["id"] for l in fid_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    if have != {r["id"] for r in fid_prompts}: sys.exit(f"REFUSED: a ZIP's fidelity50_prompts.jsonl has different prompt ids than {fid_path}")
else:
    with open(fid_path, "w", encoding="utf-8") as f:
        for r in fid_prompts: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"fidelity50 set written: {len(fid_prompts)} prompts")
fid_ids = {r["id"] for r in fid_prompts}


def build(cell, d):
    n_missing, fr, fp = 0, [], []
    for r in d["rows"]:
        pid = r["prompt_id"]
        meta = idx.get(pid)
        set_name = meta["set_name"] if meta else ("fidelity50" if pid in fid_ids else "unknown")
        if not meta and pid not in fid_ids: n_missing += 1
        rec = {"prompt_id": pid, "cell": cell, "lang": r["lang"], "set": r["set"], "set_name": set_name,
               "category": r.get("category"), "twin_id": r.get("twin_id"), "answer_script": r.get("answer_script"),
               "n_tokens": (r.get("token_usage") or {}).get("completion_tokens"), "model": f"mac:{r['cell_id']}",
               "template": r.get("template_mode"), "cache_k": r.get("cache_k"), "cache_v": r.get("cache_v"),
               "run_fingerprint": r.get("run_fingerprint"), "source": "mac", "zip": d["zip"]}
        if 'stop_token_ids' in r:
            rec['stop_token_ids'] = r['stop_token_ids']
            rec['control_vector'] = r.get('control_vector')
        fr.append(json.dumps(rec, ensure_ascii=False) + "\n")
        fp.append(json.dumps({**rec, "prompt": r["text"], "text": r["response"]}, ensure_ascii=False) + "\n")
    return "".join(fr), "".join(fp), n_missing


def same(path, text):
    return path.exists() and path.read_text(encoding="utf-8") == text  # text mode: newline-insensitive, as this script writes


built = {}
for cell, d in out_cells.items():
    priv = ROOT / "results" / "private" / cell; pub = ROOT / "results" / "cells" / cell
    recs, resp, n_missing = build(cell, d)
    built[cell] = (priv, pub, recs, resp, n_missing)
    if same(priv / "responses.jsonl", resp) and same(pub / "records.jsonl", recs): continue
    labelled = [p.name for p in (pub / "labels_qwen3guard.jsonl", pub / "labels_wildguard.jsonl",
                                 ROOT / "results" / "judges" / f"backtranslation_{cell}.jsonl") if p.exists()]
    if (priv / "responses.jsonl").exists() and labelled:
        sys.exit(f"REFUSED: {d['zip']} would change {cell}, which already has {labelled}. Nothing written. "
                 f"Move the ZIP away, or archive the old labels and answers for that cell, then re-run.")

for cell, d in out_cells.items():
    priv, pub, recs, resp, n_missing = built[cell]
    if same(priv / "responses.jsonl", resp) and same(pub / "records.jsonl", recs) and (pub / "run_info.json").exists():
        print(f"  == {cell}: {len(d['rows'])} responses, unchanged, left as is"); continue
    priv.mkdir(parents=True, exist_ok=True); pub.mkdir(parents=True, exist_ok=True)
    with open(priv / "responses.jsonl", "w", encoding="utf-8") as fp: fp.write(resp)
    with open(pub / "records.jsonl", "w", encoding="utf-8") as fr: fr.write(recs)
    json.dump({"cell": cell, "source_zip": d["zip"], "member": d["member"], "n": len(d["rows"]), "unknown_prompt_ids": n_missing,
               "sha256_zip": hashlib.sha256(Path(d["zip_path"]).read_bytes()).hexdigest(),
               **({"stop_token_ids": d["rows"][0]["stop_token_ids"], "control_vector": d["rows"][0].get("control_vector")} if "stop_token_ids" in d["rows"][0] else {})},
              open(pub / "run_info.json", "w", encoding="utf-8"), indent=1)
    print(f"  -> {cell}: {len(d['rows'])} responses, {n_missing} ids not in Datasets/final")
print("cells:", " ".join(out_cells))
