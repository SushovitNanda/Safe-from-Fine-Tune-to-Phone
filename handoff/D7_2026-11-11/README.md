# D7 hand-off (Sushovit -> Manish), 2026-11-11

Labels for the Mac GGUF cells of this delivery (2 cells), judged centrally on the laptop (plan v3: one judge, one machine). No model outputs are included.

Per cell: `labels_qwen3guard.jsonl` (safety Safe/Controversial/Unsafe, refusal Yes/No, categories; all languages),
`labels_wildguard.jsonl` (Hindi answers only: harmful_request / refusal / harmful_response yes/no via IndicTrans2 back-translation),
`records.jsonl` (text-free row per prompt: prompt_id, lang, set, set_name, n_tokens, answer_script), `run_info.json`.
Primary judge per language (PREREG amendment 1): EN and Hinglish = Qwen3Guard Unsafe (Controversial = safe; sensitivity = Unsafe or
Controversial); Hindi = WildGuard harmful_response == yes; refusal / ORR = Qwen3Guard everywhere; Hinglish ORR directional (kappa 0.31).
Join by prompt_id. `summary.json` has rates with 95 % bootstrap intervals per cell / set / language (`stats.summarise`), `summary.md` the
table and any fidelity verdict, `fidelity_<cell>.json` (and `fidelity50.json` when there is one pair) the M7 gate, counts and disagreeing prompt_ids only.
Reference FP16 rows for R(s) and DeltaDelta(s) are the laptop cells in results/drift/summary.json.

## RQ6 (M19) — central labels and laptop analysis (11 Nov, 21:45 IST)
- Both ZIPs verified against `results/mac/nov11/status.json` sha256 before import; 1612 Qwen3Guard + 554 WildGuard (back-translated Hindi) labels per cell, 0 unsure. Conventions unchanged from D7_2026-11-10.
- `laptop_rq6_analysis.json`: the 8 primary tests of MAC_PREREG_2026-11-11 plus supporting contrasts, ORR, harm split, retention, and the deployment Holm family extended to 23 tests.
- Headline (steered, Q3_K_M; ASR pooled stock 27.9 / protected 27.6 / random 27.6 %): protected − random +0.0 [−2.7, 2.7]; protected − stock −0.3 [−2.7, 2.0]. **H6 not supported.** Per language, protected − random is −6.3 [−10.3, −2.3] in English (the only RQ6 test surviving Holm in the 23-test family) and +8.3 [2.4, 14.3] in Hinglish, but protected never differs from stock: the language shifts come from the random build (random − stock EN +8.9, Hinglish −9.1). Retention 1.01 / 1.04 / 1.04 (stock / protected / random), intervals overlapping. ORR pooled general 28.4 / 24.2 / 28.0, clinical 35.6 / 41.8 / 40.5.
- Next on the Mac side: import to `results/cells/mac__rep_steer_q3km-{protected,random}`, rerun `deployment_stats.py`, `build_d8_tables.py`, figures and the D8 report; cross-check against `laptop_rq6_analysis.json`.

## Blind audit of the RQ6 labels (11 Nov, 23:30 IST) — read before writing D8
Two independent blind readers labelled 160 answers (30 discordant + 10 concordant prompts per language, EN and Hinglish, both builds). They agreed with each other on 158/160. English: judge label kept on 62/80; the random build stays the less safe one (17 vs 5 unsafe of 40 each). Hinglish: 43 of the judge's 44 "unsafe" labels were overturned, 39 of them degenerate text; 29 of 30 discordant pairs have neither answer unsafe. **So: the Hinglish per-language RQ6 contrasts (protected − random +8.3, random − stock −9.1) are a judge artefact on degenerate text and must not be interpreted. The English contrasts stand. The pooled verdict (H6 not supported) is unchanged.** Also state: protected raises clinical ORR vs stock (+6.2 pooled [1.0, 11.4], +13.7 Hindi). Counts: results/review_final/majority_vote.json.
