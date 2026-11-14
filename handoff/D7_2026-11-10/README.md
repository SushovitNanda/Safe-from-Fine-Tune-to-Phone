# D7 hand-off (Sushovit -> Manish), 2026-11-10

Labels for the Mac GGUF cells of this delivery (5 cells), judged centrally on the laptop (plan v3: one judge, one machine). No model outputs are included.

Per cell: `labels_qwen3guard.jsonl` (safety Safe/Controversial/Unsafe, refusal Yes/No, categories; all languages),
`labels_wildguard.jsonl` (Hindi answers only: harmful_request / refusal / harmful_response yes/no via IndicTrans2 back-translation),
`records.jsonl` (text-free row per prompt: prompt_id, lang, set, set_name, n_tokens, answer_script), `run_info.json`.
Primary judge per language (PREREG amendment 1): EN and Hinglish = Qwen3Guard Unsafe (Controversial = safe; sensitivity = Unsafe or
Controversial); Hindi = WildGuard harmful_response == yes; refusal / ORR = Qwen3Guard everywhere; Hinglish ORR directional (kappa 0.31).
Join by prompt_id. `summary.json` has rates with 95 % bootstrap intervals per cell / set / language (`stats.summarise`), `summary.md` the
table and any fidelity verdict, `fidelity_<cell>.json` (and `fidelity50.json` when there is one pair) the M7 gate, counts and disagreeing prompt_ids only.
Reference rows: R(s) for GGUF settings uses your Mac F16 cells as the denominator (plan v3), with the laptop FP16 values printed beside them. DeltaDelta(s) needs an original-model F16 reference; none exists on the Mac, so `laptop_gguf_analysis.json` uses the laptop FP16 cells for both models and flags it.

## Added 10 Nov 20:10: verification and laptop analysis
- All five ZIPs (and the steering fidelity ZIP) match the sha256 recorded at import, and every prompt_id in each ZIP has labels (1,612 Qwen3Guard, 554 WildGuard per full cell; 0 unsure).
- `laptop_gguf_analysis.json`: per setting, attack success with and without the vector, the vector's paired effect, retention R(s) with intervals, quantization loss and non-inferiority for both models, preamble removal, last-mile gap, DeltaDelta, over-refusal changes, Mac-vs-laptop agreement, degenerate-text rates, and a deployment Holm family. Use it to cross-check your own M20 numbers.
- Headline: the vector lowers pooled attack success by 11.0 points at F16, 12.2 at Q4_K_M, 11.1 at Q3_K_M, 9.4 without the preamble and 8.6 on the budget-phone stack (all intervals clear of zero, all surviving Holm). R = 1.11 (Q4_K_M), 1.01 (Q3_K_M), 0.85 (no preamble), 0.79 (budget-phone), every interval containing 1. The cost is clinical over-refusal, up to +8.5 points on the budget-phone stack.
