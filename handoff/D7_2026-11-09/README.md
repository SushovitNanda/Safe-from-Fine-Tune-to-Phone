# D7 hand-off (Sushovit -> Manish), 2026-11-09

Labels for the Mac GGUF cells of this delivery (1 cells), judged centrally on the laptop (plan v3: one judge, one machine). No model outputs are included.

Per cell: `labels_qwen3guard.jsonl` (safety Safe/Controversial/Unsafe, refusal Yes/No, categories; all languages),
`labels_wildguard.jsonl` (Hindi answers only: harmful_request / refusal / harmful_response yes/no via IndicTrans2 back-translation),
`records.jsonl` (text-free row per prompt: prompt_id, lang, set, set_name, n_tokens, answer_script), `run_info.json`.
Primary judge per language (PREREG amendment 1): EN and Hinglish = Qwen3Guard Unsafe (Controversial = safe; sensitivity = Unsafe or
Controversial); Hindi = WildGuard harmful_response == yes; refusal / ORR = Qwen3Guard everywhere; Hinglish ORR directional (kappa 0.31).
Join by prompt_id. `summary.json` has rates with 95 % bootstrap intervals per cell / set / language (`stats.summarise`), `summary.md` the
table and any fidelity verdict, `fidelity_<cell>.json` (and `fidelity50.json` when there is one pair) the M7 gate, counts and disagreeing prompt_ids only.
Reference FP16 rows for R(s) and DeltaDelta(s) are the laptop cells in results/drift/summary.json.
