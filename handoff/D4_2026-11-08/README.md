# D4 hand-off (Sushovit -> Manish), 8 November 2026

Source: branch code_v2.2, results of chain B (circuits v2) on the laptop, 5-6 November. Nothing here contains model outputs.

## What is in here
- `tables_per_language/{orig,med}_{en,hi,hinglish}_eap-ig_layer_x_matrix.json|csv`: 36 layers x 7 matrices in GGUF names
  (`blk.<layer>.<matrix>.weight`), with `layer_suggestions`. Scores are summed node attributions (EAP-IG, token-set metric,
  original or medical model, MLP 0 excluded), so the four attention matrices of a layer share one value and the three FFN
  matrices share another: rank at the layer x family level.
- `d4_aggregated_layer_x_matrix.json`: the ONE table to drive protection, in your exporter's schema (`layer_x_matrix`, 36 layers,
  finite scores, `layer_suggestions`). Recipe inside the file; it is the same ranking as `tensor_lists/cresta_tensors_v2_top*.json`
  (top 5 / 10 / 20 % of the 252 matrices), which Sushovit uses for circuit-restricted ReSta, so RQ4 and RQ6 share one map.
- `g3a_evidence.json` + `validation/validation_*.json`: G3a **passes** by the pre-registered rule (necessity beats all five random
  sets at k = 40): Hinglish clearly (4.70 vs 1.47), English marginally (2.46 vs 2.43), Hindi not at k = 40 (-0.82 vs 0.76; passes at
  k = 60). Sufficiency (patching original node outputs into the medical model) beats random at every k in every language.
- `overlap_jaccard.json`: top-60 overlaps and split-half floors (orig vs med within language is at/above the floor in all three
  languages; cross-language overlaps are below the EN/HI floors).
- `what_changed/`: nodes whose importance dropped most from original to medical, per language.
- `token_sets_v2.json`: the refusal / compliance opener sets behind the metric.
- `d2_hashes/{med,ctrl}/tensor_sha256.json`, `merge_info.json`: the laptop merges' per-tensor sha256 (D2 parity check).

## Caveats to carry into the method text
- The validation statistic is not monotone in k (scores are signed): at k = 20 ablating the top set *raises* refusal in EN/HI.
- The map is the ORIGINAL model's circuit (the thing to protect); the medical tables are for the what-changed comparison only.
- Hinglish's own split-half floor is low (0.28-0.35): its circuit is weakly defined by 73 pairs.

## Files
- tables_per_language\orig_en_eap-ig_layer_x_matrix.json
- tables_per_language\orig_en_eap-ig_layer_x_matrix.csv
- tables_per_language\med_en_eap-ig_layer_x_matrix.json
- tables_per_language\med_en_eap-ig_layer_x_matrix.csv
- validation\validation_en.json
- what_changed\what_changed_en.json
- tables_per_language\orig_hi_eap-ig_layer_x_matrix.json
- tables_per_language\orig_hi_eap-ig_layer_x_matrix.csv
- tables_per_language\med_hi_eap-ig_layer_x_matrix.json
- tables_per_language\med_hi_eap-ig_layer_x_matrix.csv
- validation\validation_hi.json
- what_changed\what_changed_hi.json
- tables_per_language\orig_hinglish_eap-ig_layer_x_matrix.json
- tables_per_language\orig_hinglish_eap-ig_layer_x_matrix.csv
- tables_per_language\med_hinglish_eap-ig_layer_x_matrix.json
- tables_per_language\med_hinglish_eap-ig_layer_x_matrix.csv
- validation\validation_hinglish.json
- what_changed\what_changed_hinglish.json
- overlap_jaccard.json
- tensor_lists\cresta_tensors_v2.json
- tensor_lists\cresta_tensors_v2_top10.json
- tensor_lists\cresta_tensors_v2_top20.json
- tensor_lists\cresta_tensors_v2_top5.json
- token_sets_v2.json
- d2_hashes\med\tensor_sha256.json
- d2_hashes\med\merge_info.json
- d2_hashes\ctrl\tensor_sha256.json
- d2_hashes\ctrl\merge_info.json
- d4_aggregated_layer_x_matrix.json
- g3a_evidence.json
