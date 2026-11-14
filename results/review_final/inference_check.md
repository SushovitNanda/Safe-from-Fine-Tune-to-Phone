# Inference check: do the conclusions of Report/main.tex follow from the evidence?

Date: 11 Nov 2026. Read-only review. Nothing under results/private/ was opened. No prompt or answer text is quoted.

Evidence read: results/final_stats/final.json, results/drift/summary.json, results/repair_test/summary.json,
results/final_stats/judge_validation.json, results/review_2026-11-11/intra_rater_relabel.json,
results/mac/nov11/d2_med_numeric.json, d2_ctrl_numeric.json, results/judges/kappa.json, PREREG.md, MAC_PREREG.md,
Tasks/Plan_v3.tex (hypothesis wording only).

Decision rules applied: claim = |diff| >= 5 AND 95% interval excludes 0; non-inferior = upper bound of loss < 5;
H6 = protected minus random <= -5 with interval below 0; R needs denominator >= 5.

Not checked: RQ3 numbers (overlaps, floors, necessity, sufficiency) are not in any of the listed evidence files, so the H3 row
is judged against the thesis's own tables only. The dev-sweep table (tab:sweep), the second-annotator kappas at l.429 and the Mac
degenerate rates (26.3 / 23.1 %) were not checked.

## 1. Hypotheses

| H | Thesis verdict | Follows? | Deciding numbers |
|---|---|---|---|
| H1 (Hinglish gap largest; clinical weaker) | Holds for Hinglish and for clinical harms in HI and Hinglish; overall Hindi gap "suggestive only" (l.532) | Yes, conservative on Hindi. One part untested. | G_Hinglish +15.39 [8.85, 22.01], Holm p=0.0001 rejected. G_HI +5.96 [0.33, 11.59], p=0.0412, not rejected. Clinical minus general: EN +4.71 [-3.18, 12.65] (no), HI +25.31 [15.07, 35.62], Hinglish +18.90 [7.65, 30.12], pooled +16.90 [11.20, 22.71]. |
| H2 (drift > control; largest in Hinglish and clinical) | Main claim holds; Hinglish pattern holds; harm-type pattern fails (l.629) | Yes | med-orig +18.11 [14.95, 21.26]; med-ctrl +16.36 [13.32, 19.51]; ctrl-orig +1.75 [-0.93, 4.44]. Hinglish +35.71 [28.97, 42.46]; gap change +23.8, Holm rejected. General +18.18 vs clinical +17.97. Non-degenerate: +10.92 [7.73, 14.29] (n=595), med-ctrl +9.65 [6.32, 13.16] (n=570). |
| H3 (partly shared circuit; larger changes in HI and Hinglish) | "Partly supported as a statement about structure" (l.693) | Too generous / too vague | Thesis tables only: orig-vs-med overlap 0.77 / 0.64 / 0.36 against floors 0.52-0.58 / 0.52-0.54 / 0.28-0.35, so no change beyond floor in any language; refusal metric fell most in EN (6.2 to 3.7) and least in Hinglish (6.3 to 5.5). |
| H4 (circuit-restricted patch better than whole-model) | Not supported (l.809, l.818) | Yes | Restricted 0.25: -0.58 [-3.50, 2.34]. Restricted 0.20 (late): -2.45 [-5.14, 0.23], MedMCQA 44.2. ReSta 0.05: -1.64 [-3.62, 0.35]. ReSta 0.20: -4.56 [-7.48, -1.64]. Steering 0.5: -10.05 [-12.50, -7.59]. |
| H5 (R < 1 at Q3_K_M and without preamble, most in Hinglish) | Not supported (l.895) | Yes as "not supported"; one sentence too strong | Denominator 10.98 (>= 5). R: Q3 1.011 [0.743, 1.361]; no preamble 0.851 [0.608, 1.160]; phone 0.787 [0.542, 1.111]. Hinglish R 0.92 / 1.16 / 0.76, all intervals contain 1. |
| H6 (protected beats random) | Not supported (l.971) | Yes pooled; English needs an explicit sentence | Protected-random pooled 0.00 [-2.69, 2.69]; protected-stock -0.35 [-2.69, 1.99]. R 1.011 / 1.043 / 1.043. EN protected-random -6.29 [-10.26, -2.32], p=0.0026, the only RQ6 test surviving Holm (m=23). Hinglish +8.33 [2.38, 14.29], p=0.007, not surviving. |

Notes per hypothesis.

- H1. Under the two-part rule alone the Hindi gap qualifies (5.96 >= 5, interval excludes 0). The thesis downgrades it because it fails Holm
  and reverses under the other judge (-0.7). That is weaker than the rule allows, and defensible. What is missing: H1 says the Hinglish gap is
  the *largest*, and no interval is given for G_Hinglish minus G_HI (9.4 points); the two languages also use different primary judges.
- H2. Hindi drift is not claimed on non-degenerate prompts (+4.13 [-0.41, 8.69]); the thesis says so. All of H2 rests on one fine-tune per arm, one seed.
- H3. The second clause of H3 (larger changes in Hindi and Hinglish) is not supported and is, if anything, contradicted; the verdict should say
  "not supported" for that clause instead of folding it into "partly supported". "The top-ranked nodes differ by language" is shown for EN vs HI
  only (0.36 against a floor near 0.52); the Hinglish pairs (0.21, 0.29) sit at or below the Hinglish floor (0.28-0.35) and cannot be told apart
  from noise. The gate was read at k=40, a choice logged on 9 Nov after the runs; English passes by 2.46 against 2.43.
- H4. No paired restricted-minus-whole-model contrast was computed, so "not supported" is the right strength and "no effect" (l.1069, l.1097) is
  too strong: restricted 0.20 moves Hindi by -5.63 [-9.60, -1.66], which meets the claim rule. H4 is worded about accuracy at equal safety;
  on test MedMCQA is 43.6 (restricted 0.25), 43.2 (ReSta 0.20), 45.6 (ReSta 0.10), so no accuracy advantage shows either.
- H5. "There is no loss at Q3_K_M" (l.895) is too strong: the interval allows a 26 % loss, and the steered model's Hinglish attack success is
  +8.73 [2.78, 15.48] higher at Q3_K_M than at F16 (a claimed loss; Hindi +4.64 [0.66, 8.94], not non-inferior), offset by English -5.96.
  The positive statement that the effect stays clear of zero at every setting is correct (-8.64 to -12.15, all claimed, all Holm-rejected).
  Pooled steered losses are non-inferior at all four settings (upper bounds 3.62, 4.67, 0.47, 3.04).
- H6. In English the pre-registered criterion is literally met and survives Holm. The thesis reports the number but never says so in those words.

## 2. Number check

Checked and found correct against the evidence: abstract (one exception below); Main findings paragraph; all of sec:rq6 including every cell
of tab:rq6 and the 23-test Holm statement; degeneracy paragraph; every cell of tab:degen and tab:nondeg; tab:medval; the intra-rater sentences
(26/30, 24/24, kappa 1.0 and 0.80, 11/12, 27/30, 24/5/4 of 33); the weight-parity paragraph (5 + 6 = 11 tensors, one element each,
3.8e-6 and 1.5e-5); tab:platform; tab:gguf; tab:retention; tab:ret; tab:nf4; tab:lastmile; the RQ5 verdict paragraph (0.79-1.11, lower
bounds 0.54-0.85); tab:holm (24 of 35 rejected); the Conclusion.

Mismatches.

| # | Line | Thesis | Evidence |
|---|---|---|---|
| 1 | 132 | RQ6 "test cells are still pending, so no result is claimed" | final.json rq6.available = true; results reported at l.942-971. Stale sentence. |
| 2 | 1062 (tab:confidence) | "restricted alpha=0.20 reaches -5.1" | extra_cells.cr20.vs_med.all: diff -2.45, interval [-5.14, 0.23]. -5.1 is the lower interval bound, not the effect. l.809 gives it correctly. |
| 3 | 1162 | Hinglish non-degenerate subset "65 to 77 prompts" | judge_validation.json: medical-control Hinglish n = 63 (also in tab:nondeg, l.491). Range is 63 to 77. |
| 4 | 33 (abstract) | "(retention 0.79 to 1.11, wide intervals)" after a list that starts with NF4 | NF4 retention is 1.163 [0.853, 1.593] (repair_test/summary.json; l.824 says 1.16). 0.79-1.11 covers the GGUF settings only. |
| 5 | 429 | kappa 0.80 "on the 12 harmful items both labelled (one disagreement ...)" | Numbers match the JSON (n=12, agree 11, kappa 0.8), but the same file gives 24/24 agreement where neither reading is unsure, and all four disagreements involve an unsure. The one unsafe disagreement therefore cannot be on an item "both labelled". Wording error. |
| 6 | 971 | "English (random: -6.3 ...); Hinglish (random: +8.3 ...)" | Values correct; they are protected minus random. Label garbled. |
| 7 | 1101 | "same pooled attack success as random and stock" | stock 27.92, protected 27.57, random 27.57; protected-stock -0.35 [-2.69, 1.99]. Not the same as stock, only not different. |
| 8 | 69 | weight patching: "no setting reaches the 5-point margin on test" | True pooled. Per language ReSta 0.20 EN -8.94 [-13.25, -4.64] and restricted 0.20 HI -5.63 [-9.60, -1.66] meet the rule. Add "pooled". |

Evidence files that disagree with each other (thesis follows final.json; no decision changes):
ReSta 0.05 p-values 0.0358 / 0.0936 / 0.1166 / 0.3982 in final.json holm_combined against 0.0412 / 0.0946 / 0.1228 / 0.4008 in
repair_test/summary.json; RQ2 medical-control EN p = 0.0002 (final.json) against 0.0008 (drift/summary.json holm). The scripts do not share one
bootstrap stream, which sits oddly with "shared indices and seed 13" (l.397).

Rounding only: 2.65 printed as 2.6, 27.15 as 27.1, -4.97 as -5.0 (not bold, correctly).

## 3. Internal contradictions

1. l.132 (RQ6 pending, no result claimed) against l.942-971, l.1070, l.1181 (RQ6 result reported).
2. l.1062 (-5.1) against l.809 (-2.5 [-5.1, 0.2]).
3. l.33 (retention range 0.79-1.11 attached to a list including NF4) against l.824 (NF4 1.16).
4. l.1181 "removed about half of that increase": the antecedent is the 10.9-point rise on clean answers. On non-degenerate prompts steering is
   -8.29 against +10.92 (about three quarters, on different subsets); "about 55 %" (l.33, l.69, l.807) is the all-prompt figure 10.05 / 18.11.
5. l.895 "there is no loss at Q3_K_M" against l.940 "losing up to about half of the effect cannot be ruled out", and against the claimed
   Hinglish losses at Q3_K_M (steered +8.73, medical +7.94 [3.17, 12.70]).
6. l.971 "there was little loss to recover" is true pooled (+2.10 [-0.58, 4.67]) but not in Hinglish (+8.73 claimed), and protection did not
   recover it there (60.3 against 61.1 stock).
7. l.971 "protected does not differ from stock in any language" is true for attack success only: clinical over-refusal protected minus stock is
   +6.21 [0.98, 11.44] pooled and +13.73 [5.88, 21.57] in Hindi, both meeting the claim rule (final.json rq6.orr).
8. l.1042 "Restricting ReSta to the circuit removed most of its accuracy cost" is a dev observation (42.8 against 38.5 at alpha 0.25);
   on test the restricted cell has no accuracy advantage (43.6 against 43.2 and 45.6).
9. l.1040 "a matched general fine-tune" against l.1127 "matched on tokens only".
10. l.1069 / l.1097 "no effect" for restricted ReSta against l.809 (Hindi -5.6 [-9.6, -1.7]).
11. tab:nf4 labels a pooled +4.6 [2.0, 7.1] "inferior". Under the stated rules it is "not shown non-inferior" and below the 5-point claim margin.

## 4. RQ6 interpretation

Supported as far as it goes. Protected minus stock is not clear of zero in any language (EN +2.65 [-0.33, 5.96], HI -2.98 [-6.95, 0.99],
Hinglish -0.79 [-5.95, 3.97], pooled -0.35 [-2.69, 1.99]). Random minus stock meets the claim rule in English (+8.94 [5.30, 12.58]) and
Hinglish (-9.13 [-15.48, -2.78]). So the protected-minus-random contrasts are driven by the random build.

Caveats that are missing or understated.

1. English meets the H6 criterion and survives Holm. Say so, then give the reason for discounting it.
2. Random minus stock is a supporting contrast outside the Holm family. After correction only the English protected-minus-random test stands;
   the Hinglish leg (p = 0.007) does not. "Shifts safety between languages" therefore rests on one corrected test and one uncorrected one.
3. "Does not differ from stock" is absence of evidence. The intervals allow about +6 in English and -7 in Hindi; protected is not shown
   non-inferior to stock in English (upper bound 5.96).
4. Over-refusal: protection raised clinical over-refusal against stock (contradiction 7 above). The text gives levels only.
5. No unsteered protected or random cell exists. Retention for those builds uses the unsteered *stock* Q3_K_M as reference
   (MAC_PREREG), so the test measures steered attack success, not how much of the vector's effect each build keeps. The random build's English
   "steering effect" of -0.99 [-4.97, 2.98] (R = 0.115) may be a change in the base model, not a lost repair.
6. MAC_PREREG records that the random draw shares one upgraded tensor with the protected set. The thesis does not mention it.
7. The Hinglish movement (-9.1) is in the language where most output is degenerate and the judge is weakest; it may be a change in
   degeneration, not in safety. No degeneracy rate is reported for the RQ6 cells.
8. One draw, one seed: stated at l.971 and l.1129, but the sentence before it generalises anyway.

## 5. Sentences that claim more than the evidence

Evidence base throughout: one model, one fine-tune per arm with one seed, one random draw, labels drafted and re-read by AI.

| Line | Sentence (short) | Problem |
|---|---|---|
| 971 | "Spending the same bits on random tensors shifts safety between languages without changing the pooled rate." | General causal claim from one draw; Hinglish leg fails Holm. |
| 971 | "These per-language differences come from the random build, not from protection" | Causal attribution; consistent with the data, not shown. |
| 895 | "there is no loss at Q3_K_M" | Null stated as fact; Hinglish loss is claimed. |
| 1042 | "A direction in activation space repairs more than a direction in weight space." | General law from one model and one method per kind. |
| 1042 | "ReSta's safety vector ... also carries capability, so ..." | Untested mechanism stated as cause. |
| 1040 | "Benign medical fine-tuning is a safety event ... a matched general fine-tune barely moves it." | General; one run; control matched on tokens only. |
| 627 | "Medical fine-tuning has therefore two effects: it weakens refusal, and it breaks the model's generation" | Causal and general; the control also degenerates in Hinglish (40.5 %). |
| 429 | "The approved hand labels hold up." | All checks are AI re-readings of AI drafts. |
| 818 | "partly repairs the drift without measurable utility loss" | Hindi clinical over-refusal +8.82 [1.96, 16.67] is a measured cost. |
| 1043 | "fine-tuned and original models are about equally fragile" | Equivalence from non-significant difference-in-differences (intervals reach +6). |
| 1044 | "a map that does not explain the drift is a weak guide to which tensors matter" | Speculation offered as explanation. |
| 1113 | "Prefer a run-time refusal vector to weight arithmetic" | Advice from one model, direct prompts only. |
| 530, 1111 | judge "misses about half of the unsafe Hindi answers" | Rests on about 57 Hindi items with AI-drafted labels. |
| 274 | "The merges are therefore numerically equivalent" | Evidence scope: 11 tensors differ by one F16 step in one element; say that. |
| 1059 | "Medical fine-tuning raises attack success ... High" | High for these two checkpoints; seed variance unmeasured. |

Suggested replacements for the ten that matter most.

1. l.971: "In the one random draw we ran, judged attack success was 8.9 points higher in English and 9.1 lower in Hinglish than stock, with the pooled rate unchanged. Only the English protected-minus-random contrast survives Holm correction, and one draw cannot show that random allocation does this in general."
2. l.971: "These per-language differences are consistent with a shift in the random build rather than an effect of protection: protected-minus-stock attack success is not clear of zero in any language, with intervals reaching about 6 to 7 points. The English contrast meets the H6 criterion and survives Holm correction, but we do not read it as support for H6 for that reason. Protection did raise clinical over-refusal against stock, by 6.2 points [1.0, 11.4] pooled and 13.7 [5.9, 21.6] in Hindi."
3. l.895: "no loss is measurable at Q3_K_M pooled (R = 1.01 [0.74, 1.36]), although the steered model's Hinglish attack success is 8.7 points [2.8, 15.5] higher there than at F16"
4. l.1042: "On this model and at the settings tried, a run-time refusal direction repaired more than ReSta weight arithmetic."
5. l.1042: "On dev, every ReSta alpha large enough to help also cost medical accuracy. One possible reason, which we did not test, is that the global weight difference carries capability as well as safety."
6. l.1040: "In this one fine-tune (one model, one seed), one epoch on medical exam questions doubled judged attack success, while a token-matched general fine-tune moved it by 1.8 points [-0.9, 4.4]."
7. l.627: "This medical fine-tune therefore shows two changes: fewer refusals and more degenerate output, especially in Hinglish, where the control fine-tune also degenerates (40.5 % against 64.7 %)."
8. l.429: "The approved labels are reproducible by the procedure that drafted them."
9. l.1062: "intervals near zero; restricted alpha=0.20 gives -2.5 [-5.1, 0.2] pooled"
10. l.818: "A run-time steering vector partly repairs the drift without measurable loss of MedMCQA accuracy, at the cost of Hindi clinical over-refusal 8.8 points [2.0, 16.7] above the medical model."

Also fix: l.132 (delete "its test cells are still pending, so no result is claimed" and state the null result); l.33 ("retention 0.79 to 1.16");
l.1162 ("63 to 77"); l.693 (state that the "larger changes in Hindi and Hinglish" clause of H3 is not supported).
