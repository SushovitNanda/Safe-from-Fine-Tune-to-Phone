Reference cells: orig__fp16__f16__tpl-official, med__fp16__f16__tpl-official. Repair cells stop on ids 3 and 6 (amendment 2); references are frozen cells capped at 256 tokens. Visible text agrees, token counts are not comparable. Primary repairs were fixed before generation (PREREG amendment 3); secondary cells are descriptive and outside the Holm family.

## Attack success (%, 95 % CI, test split, n = 856 pooled)

| model | pooled | en | hi | hinglish |
|---|---|---|---|---|
| Original | 18.2 [15.7, 20.8] | 11.6 [8.3, 15.2] | 17.6 [13.2, 21.9] | 27.0 [21.4, 32.5] |
| Medical | 36.3 [33.2, 39.5] | 23.5 [18.9, 28.5] | 27.1 [22.2, 32.5] | 62.7 [56.8, 68.7] |
| ReSta a0.05 | 34.7 [31.5, 38.0] | 20.9 [16.6, 25.5] | 23.5 [18.9, 28.5] | 64.7 [58.7, 70.6] |
| Steer L24 s0.5 | 26.3 [23.4, 29.2] | 15.9 [11.9, 20.2] | 13.6 [9.9, 17.6] | 54.0 [47.6, 59.9] |
| Steer L24 s1.0 | 16.9 [14.5, 19.5] | 7.3 [4.6, 10.3] | 8.3 [5.3, 11.6] | 38.9 [32.9, 44.8] |
| ReSta a0.20 | 31.8 [28.6, 34.9] | 14.6 [10.6, 18.5] | 24.2 [19.5, 29.1] | 61.5 [55.6, 67.5] |
| Restricted a0.25 top20 | 35.8 [32.6, 38.9] | 26.2 [21.2, 31.1] | 25.2 [20.5, 30.1] | 59.9 [53.6, 65.9] |
| ReSta a0.10 | 34.5 [31.3, 37.6] | 19.9 [15.6, 24.5] | 24.5 [19.9, 29.5] | 63.9 [57.9, 69.8] |

## Repair minus medical, attack success (points, paired)

| repair | pooled | en | hi | hinglish |
|---|---|---|---|---|
| ReSta a0.05 | -1.6 [-3.6, 0.3] | -2.6 [-5.3, 0.3] | -3.6 [-7.0, -0.3] | +2.0 [-2.4, 6.3] |
| Steer L24 s0.5 | -10.1 [-12.5, -7.6] **claimed** | -7.6 [-11.6, -4.0] **claimed** | -13.6 [-17.9, -9.3] **claimed** | -8.7 [-13.5, -4.4] **claimed** |
| Steer L24 s1.0 | -19.4 [-22.4, -16.4] **claimed** | -16.2 [-20.9, -11.6] **claimed** | -18.9 [-23.8, -14.2] **claimed** | -23.8 [-30.2, -17.5] **claimed** |
| ReSta a0.20 | -4.6 [-7.5, -1.6] | -8.9 [-13.2, -4.6] **claimed** | -3.0 [-7.6, 1.7] | -1.2 [-7.1, 4.8] |
| Restricted a0.25 top20 | -0.6 [-3.5, 2.3] | +2.6 [-2.0, 7.0] | -2.0 [-6.6, 2.6] | -2.8 [-8.7, 3.2] |
| ReSta a0.10 | -1.9 [-4.3, 0.7] | -3.6 [-7.6, 0.3] | -2.6 [-7.0, 1.7] | +1.2 [-4.0, 6.3] |

## Repair minus original, attack success (points, paired)

| repair | pooled | en | hi | hinglish |
|---|---|---|---|---|
| ReSta a0.05 | +16.5 [13.3, 19.6] **claimed** | +9.3 [5.3, 13.2] **claimed** | +6.0 [1.0, 10.6] **claimed** | +37.7 [30.6, 44.4] **claimed** |
| Steer L24 s0.5 | +8.1 [5.0, 11.1] **claimed** | +4.3 [0.7, 8.0] | -4.0 [-8.6, 0.7] | +27.0 [19.8, 34.1] **claimed** |
| Steer L24 s1.0 | -1.3 [-4.3, 1.6] | -4.3 [-8.3, -0.7] | -9.3 [-13.6, -5.0] **claimed** | +11.9 [4.8, 19.1] **claimed** |
| ReSta a0.20 | +13.6 [10.4, 16.7] **claimed** | +3.0 [-1.0, 7.0] | +6.6 [1.7, 11.6] **claimed** | +34.5 [27.8, 41.3] **claimed** |
| Restricted a0.25 top20 | +17.5 [14.5, 20.6] **claimed** | +14.6 [9.9, 19.2] **claimed** | +7.6 [3.0, 12.2] **claimed** | +32.9 [26.6, 39.3] **claimed** |
| ReSta a0.10 | +16.2 [13.1, 19.4] **claimed** | +8.3 [4.3, 12.2] **claimed** | +7.0 [2.0, 11.9] **claimed** | +36.9 [29.8, 44.0] **claimed** |

## Over-refusal (%, general / clinical)

| model | pooled | en | hi | hinglish (directional) |
|---|---|---|---|---|
| Original | 11.1 / 2.9 | 11.3 / 2.0 | 6.0 / 1.0 | 16.0 / 5.9 |
| Medical | 21.6 / 28.4 | 9.3 / 13.7 | 8.0 / 9.8 | 47.3 / 61.8 |
| ReSta a0.05 | 20.2 / 27.8 | 10.7 / 19.6 | 7.3 / 10.8 | 42.7 / 52.9 |
| Steer L24 s0.5 | 21.3 / 31.4 | 10.7 / 14.7 | 10.0 / 18.6 | 43.3 / 60.8 |
| Steer L24 s1.0 | 27.1 / 47.7 | 20.7 / 32.4 | 17.3 / 42.2 | 43.3 / 68.6 |
| ReSta a0.20 | 24.0 / 29.4 | 24.7 / 24.5 | 11.3 / 9.8 | 36.0 / 53.9 |
| Restricted a0.25 top20 | 22.4 / 25.2 | 10.7 / 15.7 | 9.3 / 6.9 | 47.3 / 52.9 |
| ReSta a0.10 | 18.0 / 28.4 | 11.3 / 18.6 | 6.7 / 9.8 | 36.0 / 56.9 |

## Repair minus original and minus medical, over-refusal pooled (points, paired)

| repair | general vs orig | clinical vs orig | general vs med | clinical vs med |
|---|---|---|---|---|
| ReSta a0.05 | +9.1 [4.9, 13.6] **claimed** | +24.8 [19.9, 30.1] **claimed** | -1.3 [-4.0, 1.3] | -0.7 [-4.2, 3.3] |
| Steer L24 s0.5 | +10.2 [6.0, 14.4] **claimed** | +28.4 [23.2, 33.7] **claimed** | -0.2 [-3.3, 3.1] | +2.9 [-2.0, 7.8] |
| Steer L24 s1.0 | +16.0 [11.8, 20.2] **claimed** | +44.8 [39.2, 50.3] **claimed** | +5.6 [1.3, 10.0] **claimed** | +19.3 [12.8, 25.8] **claimed** |
| ReSta a0.20 | +12.9 [8.7, 17.1] **claimed** | +26.5 [21.2, 31.7] **claimed** | +2.4 [-2.0, 6.9] | +1.0 [-4.6, 6.5] |
| Restricted a0.25 top20 | +11.3 [7.1, 15.6] **claimed** | +22.2 [17.3, 27.1] **claimed** | +0.9 [-3.1, 4.9] | -3.3 [-8.8, 2.0] |
| ReSta a0.10 | +6.9 [2.9, 11.1] **claimed** | +25.5 [20.3, 30.7] **claimed** | -3.6 [-7.1, 0.0] | +0.0 [-4.6, 4.6] |

## MedMCQA test-500 (%)

| model | accuracy | vs medical | McNemar p |
|---|---|---|---|
| Medical | 45.0 | - | - |
| Original | 40.6 | - | - |
| ReSta a0.05 | 45.4 | +0.4 | 0.774 |
| Steer L24 s0.5 | 45.4 | +0.4 | 0.688 |
| Steer L24 s1.0 | 45.4 | +0.4 | 0.625 |
| ReSta a0.20 | 43.2 | -1.8 | 0.368 |
| Restricted a0.25 top20 | 43.6 | -1.4 | 0.265 |
| ReSta a0.10 | 45.6 | +0.6 | 0.736 |
| ReSta a0.05 NF4 | 40.6 | - | - |
| Steer L24 s0.5 NF4 | 43.0 | - | - |

## Holm family (two primary repairs)

| comparison | p | rejected |
|---|---|---|
| ReSta a0.05|asr-med|en | 0.0946 | no |
| ReSta a0.05|asr-med|hi | 0.0412 | no |
| ReSta a0.05|asr-med|hinglish | 0.4008 | no |
| ReSta a0.05|asr-med|all | 0.1228 | no |
| ReSta a0.05|orr-orig|general|all | 0.0001 | yes |
| ReSta a0.05|orr-orig|clinical|all | 0.0001 | yes |
| ReSta a0.05|medmcqa-mcnemar | 0.7744 | no |
| Steer L24 s0.5|asr-med|en | 0.0002 | yes |
| Steer L24 s0.5|asr-med|hi | 0.0001 | yes |
| Steer L24 s0.5|asr-med|hinglish | 0.0001 | yes |
| Steer L24 s0.5|asr-med|all | 0.0001 | yes |
| Steer L24 s0.5|orr-orig|general|all | 0.0001 | yes |
| Steer L24 s0.5|orr-orig|clinical|all | 0.0001 | yes |
| Steer L24 s0.5|medmcqa-mcnemar | 0.6875 | no |

## NF4 retention of the repair

| repair | lang | med FP16 | rep FP16 | med NF4 | rep NF4 | R(NF4) | NF4 loss (rep) | non-inferior |
|---|---|---|---|---|---|---|---|---|
| ReSta a0.05 | en | 23.5 | 20.9 | 29.1 | 23.8 | n/a (denominator 2.6) | +3.0 [-0.7, 7.0] | no |
| ReSta a0.05 | hi | 27.1 | 23.5 | 28.5 | 25.8 | n/a (denominator 3.6) | +2.3 [-1.7, 6.3] | no |
| ReSta a0.05 | hinglish | 62.7 | 64.7 | 65.9 | 64.3 | n/a (denominator -2.0) | -0.4 [-6.0, 4.8] | yes |
| ReSta a0.05 | all | 36.3 | 34.7 | 39.7 | 36.5 | n/a (denominator 1.6) | +1.8 [-0.8, 4.3] | yes |
| Steer L24 s0.5 | en | 23.5 | 15.9 | 29.1 | 19.5 | 1.26 [0.70, 2.47] | +3.6 [0.3, 7.0] | no |
| Steer L24 s0.5 | hi | 27.1 | 13.6 | 28.5 | 14.9 | 1.00 [0.66, 1.50] | +1.3 [-2.3, 4.6] | yes |
| Steer L24 s0.5 | hinglish | 62.7 | 54.0 | 65.9 | 54.0 | 1.36 [0.67, 3.00] | +0.0 [-5.2, 5.6] | no |
| Steer L24 s0.5 | all | 36.3 | 26.3 | 39.7 | 28.0 | 1.16 [0.85, 1.59] | +1.8 [-0.6, 4.1] | yes |
