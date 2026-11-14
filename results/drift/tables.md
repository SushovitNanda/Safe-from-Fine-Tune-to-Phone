Primary judge per language (PREREG §4 / amendment 1): en: Qwen3Guard-Gen-4B, hi: WildGuard on IndicTrans2 back-translation, hinglish: Qwen3Guard-Gen-4B. Sensitivity = Qwen3Guard Unsafe or Controversial (equals the primary where WildGuard is primary).

## ASR (%; Unsafe; sensitivity in brackets) by model, harm type, language

| model | harm | all | en | hi | hinglish |
|---|---|---|---|---|---|
| orig | all | 18.2 [16,21] (25) | 11.6 [8,15] (19) | 17.6 [13,22] (18) | 27.0 [21,33] (42) |
| orig | general | 12.2 [9,15] (17) | 10.0 [6,14] (18) | 9.0 [6,13] (9) | 19.3 [13,26] (28) |
| orig | clinical | 29.1 [24,34] (39) | 14.7 [8,22] (22) | 34.3 [25,44] (34) | 38.2 [28,48] (62) |
| med | all | 36.3 [33,39] (43) | 23.5 [19,28] (28) | 27.1 [22,32] (27) | 62.7 [57,69] (80) |
| med | general | 30.4 [27,34] (37) | 22.0 [16,28] (27) | 17.5 [12,23] (18) | 58.7 [51,67] (77) |
| med | clinical | 47.1 [42,53] (54) | 26.5 [19,35] (30) | 46.1 [36,56] (46) | 68.6 [60,77] (85) |
| ctrl | all | 20.0 [17,23] (27) | 15.9 [12,20] (22) | 12.6 [9,17] (13) | 33.7 [28,40] (50) |
| ctrl | general | 15.8 [13,19] (22) | 14.0 [10,19] (20) | 6.5 [4,10] (6) | 30.7 [23,38] (44) |
| ctrl | clinical | 27.4 [23,33] (36) | 19.6 [13,27] (24) | 24.5 [17,33] (25) | 38.2 [29,48] (60) |
| orig_nf4 | all | 22.8 [20,26] (29) | 16.9 [13,21] (23) | 17.2 [13,22] (17) | 36.5 [31,42] (50) |
| orig_nf4 | general | 14.9 [12,18] (21) | 13.0 [8,18] (20) | 6.5 [4,10] (6) | 28.7 [21,36] (40) |
| orig_nf4 | clinical | 36.9 [32,42] (44) | 24.5 [17,33] (28) | 38.2 [29,48] (38) | 48.0 [38,58] (66) |
| med_nf4 | all | 39.7 [36,43] (46) | 29.1 [24,34] (34) | 28.5 [24,34] (28) | 65.9 [60,71] (81) |
| med_nf4 | general | 32.9 [29,37] (39) | 27.0 [21,34] (33) | 16.5 [12,22] (16) | 62.7 [55,70] (78) |
| med_nf4 | clinical | 52.0 [46,58] (58) | 33.3 [25,43] (36) | 52.0 [42,62] (52) | 70.6 [62,79] (85) |

## Over-refusal (%) general / clinical

| model | all | en | hi | hinglish | MedMCQA-500 | unsure |
|---|---|---|---|---|---|---|
| orig | 11.1 / 2.9 | 11.3 / 2.0 | 6.0 / 1.0 | 16.0 / 5.9 | 40.6 | 0 |
| med | 21.6 / 28.4 | 9.3 / 13.7 | 8.0 / 9.8 | 47.3 / 61.8 | 45.0 | 0 |
| ctrl | 16.2 / 9.5 | 11.3 / 2.9 | 8.7 / 2.9 | 28.7 / 22.6 | 41.0 | 0 |
| orig_nf4 | 10.0 / 3.9 | 7.3 / 0.0 | 4.0 / 0.0 | 18.7 / 11.8 | 39.2 | 0 |
| med_nf4 | 23.6 / 26.1 | 14.7 / 13.7 | 6.7 / 7.8 | 49.3 / 56.9 | 42.8 | 0 |

## RQ1 (original): language gap and clinical − general

| quantity | value | 95% CI |
|---|---|---|
| gap|hi | 5.96 | [0.33, 11.59] |
| gap|hinglish | 15.39 | [8.85, 22.01] |
| clinical_minus_general|en | 4.71 | [-3.18, 12.65] |
| clinical_minus_general|hi | 25.31 | [15.07, 35.62] |
| clinical_minus_general|hinglish | 18.9 | [7.65, 30.12] |
| clinical_minus_general|all | 16.9 | [11.2, 22.71] |

## RQ2: paired differences (points)

| comparison | diff | 95% CI | clear of 0 | ≥5 |
|---|---|---|---|---|
| med-orig|general|en | 12.0 | [7.0, 17.0] | True | True |
| med-orig|general|hi | 8.5 | [3.0, 14.0] | True | True |
| med-orig|general|hinglish | 39.33 | [30.67, 48.0] | True | True |
| med-orig|general|all | 18.18 | [14.36, 22.0] | True | True |
| med-orig|clinical|en | 11.76 | [3.92, 19.61] | True | True |
| med-orig|clinical|hi | 11.76 | [0.98, 22.55] | True | True |
| med-orig|clinical|hinglish | 30.39 | [20.59, 41.18] | True | True |
| med-orig|clinical|all | 17.97 | [12.42, 23.53] | True | True |
| med-orig|all|en | 11.92 | [7.62, 16.23] | True | True |
| med-orig|all|hi | 9.6 | [4.64, 14.57] | True | True |
| med-orig|all|hinglish | 35.71 | [28.97, 42.46] | True | True |
| med-orig|all|all | 18.11 | [14.95, 21.26] | True | True |
| med-orig|orr_general|en | -2.0 | [-7.33, 3.33] |  |  |
| med-orig|orr_general|hi | 2.0 | [-3.33, 7.33] |  |  |
| med-orig|orr_general|hinglish | 31.33 | [21.33, 41.33] |  |  |
| med-orig|orr_general|all | 10.44 | [6.22, 14.89] |  |  |
| med-orig|orr_clinical|en | 11.76 | [4.9, 18.63] |  |  |
| med-orig|orr_clinical|hi | 8.82 | [2.94, 15.69] |  |  |
| med-orig|orr_clinical|hinglish | 55.88 | [46.08, 65.69] |  |  |
| med-orig|orr_clinical|all | 25.49 | [20.59, 30.72] |  |  |
| gap_change|hi | orig 5.96 → med 3.64 (change -2.32) | | | |
| gap_change|hinglish | orig 15.39 → med 39.19 (change 23.8) | | | |
| med-ctrl|general|en | 8.0 | [2.5, 13.5] | True | True |
| med-ctrl|general|hi | 11.0 | [5.5, 16.5] | True | True |
| med-ctrl|general|hinglish | 28.0 | [20.0, 36.0] | True | True |
| med-ctrl|general|all | 14.55 | [11.09, 18.18] | True | True |
| med-ctrl|clinical|en | 6.86 | [-1.96, 15.69] | False | True |
| med-ctrl|clinical|hi | 21.57 | [10.78, 32.35] | True | True |
| med-ctrl|clinical|hinglish | 30.39 | [19.61, 41.18] | True | True |
| med-ctrl|clinical|all | 19.61 | [13.73, 25.49] | True | True |
| med-ctrl|all|en | 7.62 | [2.98, 12.25] | True | True |
| med-ctrl|all|hi | 14.57 | [9.6, 19.54] | True | True |
| med-ctrl|all|hinglish | 28.97 | [22.62, 35.32] | True | True |
| med-ctrl|all|all | 16.36 | [13.32, 19.51] | True | True |
| med-ctrl|orr_general|en | -2.0 | [-7.33, 4.0] |  |  |
| med-ctrl|orr_general|hi | -0.67 | [-4.67, 3.33] |  |  |
| med-ctrl|orr_general|hinglish | 18.67 | [8.0, 29.33] |  |  |
| med-ctrl|orr_general|all | 5.33 | [1.11, 9.56] |  |  |
| med-ctrl|orr_clinical|en | 10.78 | [3.92, 18.63] |  |  |
| med-ctrl|orr_clinical|hi | 6.86 | [0.0, 13.73] |  |  |
| med-ctrl|orr_clinical|hinglish | 39.22 | [28.43, 50.0] |  |  |
| med-ctrl|orr_clinical|all | 18.95 | [13.73, 24.18] |  |  |
| ctrl-orig|general|en | 4.0 | [0.0, 8.5] | False | False |
| ctrl-orig|general|hi | -2.5 | [-6.0, 1.0] | False | False |
| ctrl-orig|general|hinglish | 11.33 | [4.0, 19.33] | True | True |
| ctrl-orig|general|all | 3.64 | [0.73, 6.55] | True | False |
| ctrl-orig|clinical|en | 4.9 | [-1.96, 11.76] | False | False |
| ctrl-orig|clinical|hi | -9.8 | [-18.63, -1.96] | True | True |
| ctrl-orig|clinical|hinglish | 0.0 | [-10.78, 10.78] | False | False |
| ctrl-orig|clinical|all | -1.63 | [-6.86, 3.59] | False | False |
| ctrl-orig|all|en | 4.3 | [0.66, 7.95] | True | False |
| ctrl-orig|all|hi | -4.97 | [-8.94, -1.32] | True | False |
| ctrl-orig|all|hinglish | 6.75 | [0.4, 13.1] | True | True |
| ctrl-orig|all|all | 1.75 | [-0.93, 4.44] | False | False |
| ctrl-orig|orr_general|en | 0.0 | [-4.0, 4.0] |  |  |
| ctrl-orig|orr_general|hi | 2.67 | [-1.33, 6.67] |  |  |
| ctrl-orig|orr_general|hinglish | 12.67 | [4.67, 21.33] |  |  |
| ctrl-orig|orr_general|all | 5.11 | [1.78, 8.44] |  |  |
| ctrl-orig|orr_clinical|en | 0.98 | [-1.96, 4.9] |  |  |
| ctrl-orig|orr_clinical|hi | 1.96 | [0.0, 4.9] |  |  |
| ctrl-orig|orr_clinical|hinglish | 16.67 | [8.82, 25.49] |  |  |
| ctrl-orig|orr_clinical|all | 6.54 | [3.27, 9.8] |  |  |

## RQ5 at NF4

| quantity | value | 95% CI | note |
|---|---|---|---|
| deltadelta|en | 0.33 | [-4.3, 4.97] |  |
| nf4_loss|orig|en | 5.3 | [2.32, 8.28] | inferior |
| nf4_loss|med|en | 5.63 | [1.66, 9.6] | inferior |
| deltadelta|hi | 1.66 | [-4.64, 7.62] |  |
| nf4_loss|orig|hi | -0.33 | [-4.3, 3.64] | non-inferior |
| nf4_loss|med|hi | 1.32 | [-2.98, 5.63] |  |
| deltadelta|hinglish | -6.35 | [-14.68, 1.59] |  |
| nf4_loss|orig|hinglish | 9.52 | [3.17, 15.87] | inferior |
| nf4_loss|med|hinglish | 3.17 | [-2.38, 8.73] |  |
| deltadelta|all | -1.17 | [-4.79, 2.45] |  |
| nf4_loss|orig|all | 4.56 | [1.99, 7.13] | inferior |
| nf4_loss|med|all | 3.39 | [0.82, 5.96] | inferior |

## Holm family

| test | bootstrap p | reject (Holm) |
|---|---|---|
| rq2:med-orig|general|all | 0.0001 | True |
| rq2:med-orig|clinical|all | 0.0001 | True |
| rq2:med-orig|all|en | 0.0001 | True |
| rq2:med-orig|all|hi | 0.0002 | True |
| rq2:med-orig|all|hinglish | 0.0001 | True |
| rq2:med-orig|all|all | 0.0001 | True |
| rq2:med-ctrl|general|all | 0.0001 | True |
| rq2:med-ctrl|clinical|all | 0.0001 | True |
| rq2:med-ctrl|all|en | 0.0008 | True |
| rq2:med-ctrl|all|hi | 0.0001 | True |
| rq2:med-ctrl|all|hinglish | 0.0001 | True |
| rq2:med-ctrl|all|all | 0.0001 | True |
| rq5:deltadelta|all | 0.555 | False |
