# Independent re-derivation of headline statistics

Standalone script `results/review_final/independent_stats.py` (numpy only, seed 20261111, 10000 resamples, unstratified percentile bootstrap over prompts within each subset).

Subset sizes: harmful all=856, en=302, hi=302, hinglish=252; benign general=450, clinical=306.

Tolerances: point > 0.05, CI bound > 0.5, R > 0.01 (R CI bound > 0.05, my own choice).

**170 quantities; 170 compared with project files; 0 mismatches.**

CI-bound agreement (rates and paired differences, 328 bounds): max |dev| = 0.40; 47 bounds differ by more than 0.3; 77 differ at all (2 dp). Largest: B paired cresta20-med / hinglish hi 3.57 vs 3.17; D ASR mac med q4km / hinglish hi 69.84 vs 69.44; D ASR mac steer q4km / hinglish lo 50.00 vs 49.6; D paired steer_budget-phone-med_budget-phone / hinglish hi -2.38 vs -2.78; B ASR cresta25 fp16 / hinglish lo 53.97 vs 53.57; B paired resta05-med / hinglish hi 5.95 vs 6.35.

## Data integrity

- No issues across 23 cells: every cell has the same 1612 prompt ids, no duplicates, only expected label values, every hi harmful prompt has a WildGuard label.

## Table

| sec | quantity | mine (est [95% CI]) | project | match? |
|---|---|---|---|---|
| A | ASR orig fp16 / all | 18.22 [15.65, 20.79] | 18.22 [15.65, 20.79] | match |
| A | ASR orig fp16 / en | 11.59 [7.95, 15.23] | 11.59 [8.28, 15.23] | match |
| A | ASR orig fp16 / hi | 17.55 [13.25, 21.85] | 17.55 [13.25, 21.85] | match |
| A | ASR orig fp16 / hinglish | 26.98 [21.83, 32.54] | 26.98 [21.43, 32.54] | match |
| A | ASR ctrl fp16 / all | 19.98 [17.29, 22.66] | 19.98 [17.41, 22.66] | match |
| A | ASR ctrl fp16 / en | 15.89 [11.92, 20.20] | 15.89 [11.92, 20.20] | match |
| A | ASR ctrl fp16 / hi | 12.58 [8.94, 16.56] | 12.58 [8.94, 16.56] | match |
| A | ASR ctrl fp16 / hinglish | 33.73 [28.17, 39.68] | 33.73 [27.78, 39.68] | match |
| A | ASR med fp16 / all | 36.33 [33.17, 39.60] | 36.33 [33.18, 39.49] | match |
| A | ASR med fp16 / en | 23.51 [18.87, 28.48] | 23.51 [18.87, 28.48] | match |
| A | ASR med fp16 / hi | 27.15 [22.19, 32.12] | 27.15 [22.19, 32.45] | match |
| A | ASR med fp16 / hinglish | 62.70 [56.75, 68.65] | 62.70 [56.75, 68.65] | match |
| A | paired med-orig / all | 18.11 [14.95, 21.26] | 18.11 [14.95, 21.26] | match |
| A | paired med-orig / en | 11.92 [7.62, 16.23] | 11.92 [7.62, 16.23] | match |
| A | paired med-orig / hi | 9.60 [4.64, 14.90] | 9.60 [4.64, 14.57] | match |
| A | paired med-orig / hinglish | 35.71 [28.97, 42.46] | 35.71 [28.97, 42.46] | match |
| A | paired med-ctrl / all | 16.36 [13.32, 19.39] | 16.36 [13.32, 19.51] | match |
| A | paired med-ctrl / en | 7.62 [2.98, 12.25] | 7.62 [2.98, 12.25] | match |
| A | paired med-ctrl / hi | 14.57 [9.60, 19.54] | 14.57 [9.60, 19.54] | match |
| A | paired med-ctrl / hinglish | 28.97 [22.62, 35.32] | 28.97 [22.62, 35.32] | match |
| A | paired ctrl-orig / all | 1.75 [-0.82, 4.44] | 1.75 [-0.93, 4.44] | match |
| A | paired ctrl-orig / en | 4.30 [0.66, 7.95] | 4.30 [0.66, 7.95] | match |
| A | paired ctrl-orig / hi | -4.97 [-8.94, -1.32] | -4.97 [-8.94, -1.32] | match |
| A | paired ctrl-orig / hinglish | 6.75 [0.40, 13.10] | 6.75 [0.40, 13.10] | match |
| B | ASR steer fp16 / all | 26.29 [23.36, 29.32] | 26.29 [23.36, 29.21] | match |
| B | paired steer-med / all | -10.05 [-12.50, -7.59] | -10.05 [-12.50, -7.59] | match |
| B | ASR steer fp16 / en | 15.89 [11.92, 20.20] | 15.89 [11.92, 20.20] | match |
| B | paired steer-med / en | -7.62 [-11.59, -3.64] | -7.62 [-11.59, -3.97] | match |
| B | ASR steer fp16 / hi | 13.58 [9.60, 17.55] | 13.58 [9.93, 17.55] | match |
| B | paired steer-med / hi | -13.58 [-17.88, -9.27] | -13.58 [-17.88, -9.27] | match |
| B | ASR steer fp16 / hinglish | 53.97 [47.62, 60.32] | 53.97 [47.62, 59.92] | match |
| B | paired steer-med / hinglish | -8.73 [-13.49, -4.37] | -8.73 [-13.49, -4.37] | match |
| B | ASR resta05 fp16 / all | 34.70 [31.54, 37.97] | 34.70 [31.54, 37.97] | match |
| B | paired resta05-med / all | -1.64 [-3.62, 0.35] | -1.64 [-3.62, 0.35] | match |
| B | ASR resta05 fp16 / en | 20.86 [16.23, 25.50] | 20.86 [16.55, 25.50] | match |
| B | paired resta05-med / en | -2.65 [-5.63, 0.33] | -2.65 [-5.31, 0.33] | match |
| B | ASR resta05 fp16 / hi | 23.51 [18.54, 28.48] | 23.51 [18.87, 28.48] | match |
| B | paired resta05-med / hi | -3.64 [-6.95, -0.33] | -3.64 [-6.95, -0.33] | match |
| B | ASR resta05 fp16 / hinglish | 64.68 [58.73, 70.63] | 64.68 [58.73, 70.63] | match |
| B | paired resta05-med / hinglish | 1.98 [-2.38, 5.95] | 1.98 [-2.38, 6.35] | match |
| B | ASR resta20 fp16 / all | 31.78 [28.74, 34.81] | 31.78 [28.62, 34.93] | match |
| B | paired resta20-med / all | -4.56 [-7.36, -1.64] | -4.56 [-7.48, -1.64] | match |
| B | ASR resta20 fp16 / en | 14.57 [10.60, 18.54] | 14.57 [10.60, 18.54] | match |
| B | paired resta20-med / en | -8.94 [-13.25, -4.64] | -8.94 [-13.25, -4.64] | match |
| B | ASR resta20 fp16 / hi | 24.17 [19.54, 29.14] | 24.17 [19.54, 29.14] | match |
| B | paired resta20-med / hi | -2.98 [-7.62, 1.66] | -2.98 [-7.62, 1.66] | match |
| B | ASR resta20 fp16 / hinglish | 61.51 [55.56, 67.46] | 61.51 [55.56, 67.46] | match |
| B | paired resta20-med / hinglish | -1.19 [-7.14, 4.76] | -1.19 [-7.14, 4.76] | match |
| B | ASR cresta25 fp16 / all | 35.75 [32.48, 38.90] | 35.75 [32.59, 38.90] | match |
| B | paired cresta25-med / all | -0.58 [-3.50, 2.34] | -0.58 [-3.50, 2.34] | match |
| B | ASR cresta25 fp16 / en | 26.16 [21.19, 31.13] | 26.16 [21.19, 31.13] | match |
| B | paired cresta25-med / en | 2.65 [-1.66, 6.95] | 2.65 [-1.99, 6.95] | match |
| B | ASR cresta25 fp16 / hi | 25.17 [20.20, 30.13] | 25.17 [20.53, 30.13] | match |
| B | paired cresta25-med / hi | -1.99 [-6.62, 2.65] | -1.99 [-6.62, 2.65] | match |
| B | ASR cresta25 fp16 / hinglish | 59.92 [53.97, 65.87] | 59.92 [53.57, 65.87] | match |
| B | paired cresta25-med / hinglish | -2.78 [-8.73, 3.17] | -2.78 [-8.73, 3.17] | match |
| B | ASR cresta20 fp16 / all | 33.88 [30.72, 37.03] | 33.88 [30.72, 37.03] | match |
| B | paired cresta20-med / all | -2.45 [-5.14, 0.23] | -2.45 [-5.14, 0.23] | match |
| B | ASR cresta20 fp16 / en | 24.17 [19.54, 29.14] | 24.17 [19.54, 28.81] | match |
| B | paired cresta20-med / en | 0.66 [-3.32, 4.64] | 0.66 [-3.64, 4.97] | match |
| B | ASR cresta20 fp16 / hi | 21.52 [16.89, 26.16] | 21.52 [16.89, 26.16] | match |
| B | paired cresta20-med / hi | -5.63 [-9.93, -1.66] | -5.63 [-9.60, -1.66] | match |
| B | ASR cresta20 fp16 / hinglish | 60.32 [54.37, 66.27] | 60.32 [54.37, 66.27] | match |
| B | paired cresta20-med / hinglish | -2.38 [-8.33, 3.57] | -2.38 [-8.33, 3.17] | match |
| C | ASR orig_nf4 / all | 22.78 [19.98, 25.58] | 22.78 [19.98, 25.58] | match |
| C | ASR med_nf4 / all | 39.72 [36.45, 42.99] | 39.72 [36.45, 42.99] | match |
| C | ASR steer_nf4 / all | 28.04 [25.12, 31.07] | 28.04 [no CI stored] | match |
| C | paired orig_nf4-orig / all | 4.56 [1.99, 7.13] | 4.56 [1.99, 7.13] | match |
| C | paired med_nf4-med / all | 3.39 [0.82, 5.96] | 3.39 [0.82, 5.96] | match |
| C | paired steer_nf4-med_nf4 / all | -11.68 [-14.25, -9.00] | -11.68 [no CI stored] | match |
| D | ASR mac med f16 / all | 36.80 [33.53, 40.07] | 36.80 [33.53, 39.95] | match |
| D | ASR mac steer f16 / all | 25.82 [22.90, 28.74] | 25.82 [22.90, 28.74] | match |
| D | paired steer_f16-med_f16 / all | -10.98 [-13.55, -8.41] | -10.98 [-13.55, -8.53] | match |
| D | ASR mac med f16 / en | 24.83 [19.87, 29.80] | 24.83 [19.87, 29.80] | match |
| D | ASR mac steer f16 / en | 16.23 [12.25, 20.53] | 16.23 [12.25, 20.53] | match |
| D | paired steer_f16-med_f16 / en | -8.61 [-12.58, -4.64] | -8.61 [-12.58, -4.64] | match |
| D | ASR mac med f16 / hi | 27.48 [22.52, 32.45] | 27.48 [22.52, 32.45] | match |
| D | ASR mac steer f16 / hi | 13.25 [9.60, 17.22] | 13.25 [9.60, 17.22] | match |
| D | paired steer_f16-med_f16 / hi | -14.24 [-18.54, -9.93] | -14.24 [-18.54, -10.26] | match |
| D | ASR mac med f16 / hinglish | 62.30 [56.35, 68.25] | 62.30 [56.35, 68.25] | match |
| D | ASR mac steer f16 / hinglish | 52.38 [46.03, 58.73] | 52.38 [46.03, 58.73] | match |
| D | paired steer_f16-med_f16 / hinglish | -9.92 [-14.68, -5.16] | -9.92 [-14.68, -5.16] | match |
| D | ASR mac med q4km / all | 39.37 [36.21, 42.64] | 39.37 [36.10, 42.64] | match |
| D | ASR mac steer q4km / all | 27.22 [24.30, 30.14] | 27.22 [24.18, 30.26] | match |
| D | paired steer_q4km-med_q4km / all | -12.15 [-15.07, -9.35] | -12.15 [-15.07, -9.35] | match |
| D | ASR mac med q4km / en | 28.15 [23.18, 33.44] | 28.15 [23.18, 33.11] | match |
| D | ASR mac steer q4km / en | 16.89 [12.58, 21.19] | 16.89 [12.91, 21.19] | match |
| D | paired steer_q4km-med_q4km / en | -11.26 [-15.56, -6.95] | -11.26 [-15.56, -6.95] | match |
| D | ASR mac med q4km / hi | 30.13 [24.83, 35.43] | 30.13 [25.17, 35.43] | match |
| D | ASR mac steer q4km / hi | 13.58 [9.93, 17.55] | 13.58 [9.93, 17.55] | match |
| D | paired steer_q4km-med_q4km / hi | -16.56 [-21.19, -11.92] | -16.56 [-21.19, -12.25] | match |
| D | ASR mac med q4km / hinglish | 63.89 [57.94, 69.84] | 63.89 [57.94, 69.44] | match |
| D | ASR mac steer q4km / hinglish | 55.95 [50.00, 61.90] | 55.95 [49.60, 61.90] | match |
| D | paired steer_q4km-med_q4km / hinglish | -7.94 [-13.89, -1.98] | -7.94 [-13.89, -1.98] | match |
| D | ASR mac med q3km / all | 39.02 [35.75, 42.29] | 39.02 [35.75, 42.17] | match |
| D | ASR mac steer q3km / all | 27.92 [25.00, 30.96] | 27.92 [24.88, 30.96] | match |
| D | paired steer_q3km-med_q3km / all | -11.10 [-13.79, -8.41] | -11.10 [-13.79, -8.41] | match |
| D | ASR mac med q3km / en | 20.20 [15.89, 24.83] | 20.20 [15.89, 24.83] | match |
| D | ASR mac steer q3km / en | 10.26 [6.95, 13.91] | 10.26 [6.95, 13.91] | match |
| D | paired steer_q3km-med_q3km / en | -9.93 [-13.91, -6.29] | -9.93 [-13.91, -6.29] | match |
| D | ASR mac med q3km / hi | 31.79 [26.49, 37.09] | 31.79 [26.82, 37.09] | match |
| D | ASR mac steer q3km / hi | 17.88 [13.58, 22.19] | 17.88 [13.58, 22.19] | match |
| D | paired steer_q3km-med_q3km / hi | -13.91 [-18.54, -9.27] | -13.91 [-18.54, -9.27] | match |
| D | ASR mac med q3km / hinglish | 70.24 [64.68, 75.79] | 70.24 [64.68, 75.79] | match |
| D | ASR mac steer q3km / hinglish | 61.11 [55.16, 67.06] | 61.11 [55.16, 67.06] | match |
| D | paired steer_q3km-med_q3km / hinglish | -9.13 [-14.68, -3.57] | -9.13 [-14.68, -3.96] | match |
| D | ASR mac med q4km-nopre / all | 33.18 [30.02, 36.45] | 33.18 [30.02, 36.33] | match |
| D | ASR mac steer q4km-nopre / all | 23.83 [21.03, 26.64] | 23.83 [21.03, 26.75] | match |
| D | paired steer_q4km-nopre-med_q4km-nopre / all | -9.35 [-11.92, -6.78] | -9.35 [-11.92, -6.78] | match |
| D | ASR mac med q4km-nopre / en | 19.21 [14.90, 23.84] | 19.21 [14.90, 23.84] | match |
| D | ASR mac steer q4km-nopre / en | 12.91 [9.27, 16.89] | 12.91 [9.27, 16.89] | match |
| D | paired steer_q4km-nopre-med_q4km-nopre / en | -6.29 [-10.26, -2.32] | -6.29 [-10.26, -2.32] | match |
| D | ASR mac med q4km-nopre / hi | 24.17 [19.54, 29.14] | 24.17 [19.54, 29.14] | match |
| D | ASR mac steer q4km-nopre / hi | 13.58 [9.60, 17.55] | 13.58 [9.93, 17.55] | match |
| D | paired steer_q4km-nopre-med_q4km-nopre / hi | -10.60 [-14.90, -6.29] | -10.60 [-15.23, -6.29] | match |
| D | ASR mac med q4km-nopre / hinglish | 60.71 [54.76, 66.67] | 60.71 [54.76, 66.67] | match |
| D | ASR mac steer q4km-nopre / hinglish | 49.21 [42.86, 55.56] | 49.21 [42.86, 55.56] | match |
| D | paired steer_q4km-nopre-med_q4km-nopre / hinglish | -11.51 [-16.27, -6.75] | -11.51 [-16.27, -6.75] | match |
| D | ASR mac med budget-phone / all | 34.81 [31.66, 38.08] | 34.81 [31.54, 37.97] | match |
| D | ASR mac steer budget-phone / all | 26.17 [23.25, 29.21] | 26.17 [23.25, 29.09] | match |
| D | paired steer_budget-phone-med_budget-phone / all | -8.64 [-11.10, -6.07] | -8.64 [-11.10, -6.19] | match |
| D | ASR mac med budget-phone / en | 16.89 [12.58, 21.19] | 16.89 [12.91, 21.19] | match |
| D | ASR mac steer budget-phone / en | 9.93 [6.62, 13.58] | 9.93 [6.62, 13.25] | match |
| D | paired steer_budget-phone-med_budget-phone / en | -6.95 [-10.93, -3.31] | -6.95 [-10.60, -3.31] | match |
| D | ASR mac med budget-phone / hi | 26.49 [21.52, 31.46] | 26.49 [21.52, 31.46] | match |
| D | ASR mac steer budget-phone / hi | 15.23 [11.26, 19.21] | 15.23 [11.26, 19.21] | match |
| D | paired steer_budget-phone-med_budget-phone / hi | -11.26 [-15.56, -6.95] | -11.26 [-15.56, -6.95] | match |
| D | ASR mac med budget-phone / hinglish | 66.27 [60.32, 71.83] | 66.27 [60.32, 71.83] | match |
| D | ASR mac steer budget-phone / hinglish | 58.73 [52.78, 64.68] | 58.73 [52.78, 64.69] | match |
| D | paired steer_budget-phone-med_budget-phone / hinglish | -7.54 [-12.70, -2.38] | -7.54 [-12.70, -2.78] | match |
| D | retention R q4km / all | 1.106 [0.847, 1.454] | 1.106 [0.847, 1.446] | match |
| D | retention R q3km / all | 1.011 [0.753, 1.368] | 1.011 [0.743, 1.361] | match |
| D | retention R q4km-nopre / all | 0.851 [0.607, 1.161] | 0.851 [0.608, 1.160] | match |
| D | retention R budget-phone / all | 0.787 [0.541, 1.110] | 0.787 [0.542, 1.111] | match |
| E | ASR q3km stock / all | 27.92 [25.00, 30.96] | 27.92 [24.88, 30.96] | match |
| E | ASR q3km stock / en | 10.26 [6.95, 13.91] | 10.26 [6.95, 13.91] | match |
| E | ASR q3km stock / hi | 17.88 [13.58, 22.19] | 17.88 [13.58, 22.19] | match |
| E | ASR q3km stock / hinglish | 61.11 [55.16, 67.06] | 61.11 [55.16, 67.06] | match |
| E | ASR q3km protected / all | 27.57 [24.53, 30.61] | 27.57 [24.53, 30.61] | match |
| E | ASR q3km protected / en | 12.91 [9.27, 16.89] | 12.91 [9.27, 16.89] | match |
| E | ASR q3km protected / hi | 14.90 [10.93, 18.87] | 14.90 [10.93, 18.87] | match |
| E | ASR q3km protected / hinglish | 60.32 [54.37, 66.27] | 60.32 [54.37, 66.27] | match |
| E | ASR q3km random / all | 27.57 [24.65, 30.61] | 27.57 [24.53, 30.61] | match |
| E | ASR q3km random / en | 19.21 [14.90, 23.84] | 19.21 [14.90, 23.51] | match |
| E | ASR q3km random / hi | 15.56 [11.59, 19.54] | 15.56 [11.59, 19.87] | match |
| E | ASR q3km random / hinglish | 51.98 [45.63, 57.94] | 51.98 [45.63, 58.33] | match |
| E | paired protected-random / all | 0.00 [-2.69, 2.57] | 0.00 [-2.69, 2.69] | match |
| E | paired protected-random / en | -6.29 [-10.60, -2.32] | -6.29 [-10.26, -2.32] | match |
| E | paired protected-random / hi | -0.66 [-4.30, 2.98] | -0.66 [-4.30, 2.98] | match |
| E | paired protected-random / hinglish | 8.33 [2.38, 14.29] | 8.33 [2.38, 14.29] | match |
| E | paired protected-stock / all | -0.35 [-2.69, 1.99] | -0.35 [-2.69, 1.99] | match |
| E | paired protected-stock / en | 2.65 [-0.66, 5.96] | 2.65 [-0.33, 5.96] | match |
| E | paired protected-stock / hi | -2.98 [-6.95, 0.66] | -2.98 [-6.95, 0.99] | match |
| E | paired protected-stock / hinglish | -0.79 [-5.56, 4.37] | -0.79 [-5.95, 3.97] | match |
| E | paired random-stock / all | -0.35 [-3.04, 2.34] | -0.35 [-3.04, 2.34] | match |
| E | paired random-stock / en | 8.94 [5.30, 12.91] | 8.94 [5.30, 12.58] | match |
| E | paired random-stock / hi | -2.32 [-6.62, 1.66] | -2.32 [-6.29, 1.66] | match |
| E | paired random-stock / hinglish | -9.13 [-15.48, -2.78] | -9.13 [-15.48, -2.78] | match |
| F | ORR orig fp16 / general | 11.11 [8.22, 14.00] | 11.11 [8.22, 14.22] | match |
| F | ORR orig fp16 / clinical | 2.94 [1.31, 4.90] | 2.94 [1.31, 4.90] | match |
| F | ORR med fp16 / general | 21.56 [17.78, 25.33] | 21.56 [17.78, 25.33] | match |
| F | ORR med fp16 / clinical | 28.43 [23.53, 33.66] | 28.43 [23.53, 33.66] | match |
| F | ORR steer fp16 / general | 21.33 [17.56, 25.11] | 21.33 [17.56, 25.11] | match |
| F | ORR steer fp16 / clinical | 31.37 [26.47, 36.60] | 31.37 [26.14, 36.60] | match |
| F | ORR q3km stock / general | 28.44 [24.22, 32.67] | 28.44 [24.22, 32.67] | match |
| F | ORR q3km stock / clinical | 35.62 [30.07, 40.85] | 35.62 [30.39, 40.85] | match |
| F | ORR q3km protected / general | 24.22 [20.22, 28.22] | 24.22 [20.22, 28.22] | match |
| F | ORR q3km protected / clinical | 41.83 [36.27, 47.39] | 41.83 [36.27, 47.39] | match |
| F | ORR q3km random / general | 28.00 [23.78, 32.00] | 28.00 [23.99, 32.22] | match |
| F | ORR q3km random / clinical | 40.52 [34.97, 46.08] | 40.52 [34.97, 46.08] | match |

## Retention detail (pooled)

| X | my numerator | my denominator | project num | project den | resamples with den <= 0 |
|---|---|---|---|---|---|
| q4km | 12.15 | 10.98 | 12.15 | 10.98 | 0 |
| q3km | 11.10 | 10.98 | 11.1 | 10.98 | 0 |
| q4km-nopre | 9.35 | 10.98 | 9.35 | 10.98 | 0 |
| budget-phone | 8.64 | 10.98 | 8.64 | 10.98 | 0 |

## Mismatches

None.

## Claim rule (|diff| >= 5 and CI excludes 0)

| paired difference | diff [95% CI] | claimed (mine) | claimed (project) |
|---|---|---|---|
| A paired med-orig / all | 18.11 [14.95, 21.26] | YES | YES |
| A paired med-orig / en | 11.92 [7.62, 16.23] | YES | YES |
| A paired med-orig / hi | 9.60 [4.64, 14.90] | YES | YES |
| A paired med-orig / hinglish | 35.71 [28.97, 42.46] | YES | YES |
| A paired med-ctrl / all | 16.36 [13.32, 19.39] | YES | YES |
| A paired med-ctrl / en | 7.62 [2.98, 12.25] | YES | YES |
| A paired med-ctrl / hi | 14.57 [9.60, 19.54] | YES | YES |
| A paired med-ctrl / hinglish | 28.97 [22.62, 35.32] | YES | YES |
| A paired ctrl-orig / all | 1.75 [-0.82, 4.44] | no | no |
| A paired ctrl-orig / en | 4.30 [0.66, 7.95] | no | no |
| A paired ctrl-orig / hi | -4.97 [-8.94, -1.32] | no | no |
| A paired ctrl-orig / hinglish | 6.75 [0.40, 13.10] | YES | YES |
| B paired steer-med / all | -10.05 [-12.50, -7.59] | YES | YES |
| B paired steer-med / en | -7.62 [-11.59, -3.64] | YES | YES |
| B paired steer-med / hi | -13.58 [-17.88, -9.27] | YES | YES |
| B paired steer-med / hinglish | -8.73 [-13.49, -4.37] | YES | YES |
| B paired resta05-med / all | -1.64 [-3.62, 0.35] | no | no |
| B paired resta05-med / en | -2.65 [-5.63, 0.33] | no | no |
| B paired resta05-med / hi | -3.64 [-6.95, -0.33] | no | no |
| B paired resta05-med / hinglish | 1.98 [-2.38, 5.95] | no | no |
| B paired resta20-med / all | -4.56 [-7.36, -1.64] | no | no |
| B paired resta20-med / en | -8.94 [-13.25, -4.64] | YES | YES |
| B paired resta20-med / hi | -2.98 [-7.62, 1.66] | no | no |
| B paired resta20-med / hinglish | -1.19 [-7.14, 4.76] | no | no |
| B paired cresta25-med / all | -0.58 [-3.50, 2.34] | no | no |
| B paired cresta25-med / en | 2.65 [-1.66, 6.95] | no | no |
| B paired cresta25-med / hi | -1.99 [-6.62, 2.65] | no | no |
| B paired cresta25-med / hinglish | -2.78 [-8.73, 3.17] | no | no |
| B paired cresta20-med / all | -2.45 [-5.14, 0.23] | no | no |
| B paired cresta20-med / en | 0.66 [-3.32, 4.64] | no | no |
| B paired cresta20-med / hi | -5.63 [-9.93, -1.66] | YES | YES |
| B paired cresta20-med / hinglish | -2.38 [-8.33, 3.57] | no | no |
| C paired orig_nf4-orig / all | 4.56 [1.99, 7.13] | no | n/a |
| C paired med_nf4-med / all | 3.39 [0.82, 5.96] | no | n/a |
| C paired steer_nf4-med_nf4 / all | -11.68 [-14.25, -9.00] | YES | n/a |
| D paired steer_f16-med_f16 / all | -10.98 [-13.55, -8.41] | YES | YES |
| D paired steer_f16-med_f16 / en | -8.61 [-12.58, -4.64] | YES | YES |
| D paired steer_f16-med_f16 / hi | -14.24 [-18.54, -9.93] | YES | YES |
| D paired steer_f16-med_f16 / hinglish | -9.92 [-14.68, -5.16] | YES | YES |
| D paired steer_q4km-med_q4km / all | -12.15 [-15.07, -9.35] | YES | YES |
| D paired steer_q4km-med_q4km / en | -11.26 [-15.56, -6.95] | YES | YES |
| D paired steer_q4km-med_q4km / hi | -16.56 [-21.19, -11.92] | YES | YES |
| D paired steer_q4km-med_q4km / hinglish | -7.94 [-13.89, -1.98] | YES | YES |
| D paired steer_q3km-med_q3km / all | -11.10 [-13.79, -8.41] | YES | YES |
| D paired steer_q3km-med_q3km / en | -9.93 [-13.91, -6.29] | YES | YES |
| D paired steer_q3km-med_q3km / hi | -13.91 [-18.54, -9.27] | YES | YES |
| D paired steer_q3km-med_q3km / hinglish | -9.13 [-14.68, -3.57] | YES | YES |
| D paired steer_q4km-nopre-med_q4km-nopre / all | -9.35 [-11.92, -6.78] | YES | YES |
| D paired steer_q4km-nopre-med_q4km-nopre / en | -6.29 [-10.26, -2.32] | YES | YES |
| D paired steer_q4km-nopre-med_q4km-nopre / hi | -10.60 [-14.90, -6.29] | YES | YES |
| D paired steer_q4km-nopre-med_q4km-nopre / hinglish | -11.51 [-16.27, -6.75] | YES | YES |
| D paired steer_budget-phone-med_budget-phone / all | -8.64 [-11.10, -6.07] | YES | YES |
| D paired steer_budget-phone-med_budget-phone / en | -6.95 [-10.93, -3.31] | YES | YES |
| D paired steer_budget-phone-med_budget-phone / hi | -11.26 [-15.56, -6.95] | YES | YES |
| D paired steer_budget-phone-med_budget-phone / hinglish | -7.54 [-12.70, -2.38] | YES | YES |
| E paired protected-random / all | 0.00 [-2.69, 2.57] | no | no |
| E paired protected-random / en | -6.29 [-10.60, -2.32] | YES | YES |
| E paired protected-random / hi | -0.66 [-4.30, 2.98] | no | no |
| E paired protected-random / hinglish | 8.33 [2.38, 14.29] | YES | YES |
| E paired protected-stock / all | -0.35 [-2.69, 1.99] | no | no |
| E paired protected-stock / en | 2.65 [-0.66, 5.96] | no | no |
| E paired protected-stock / hi | -2.98 [-6.95, 0.66] | no | no |
| E paired protected-stock / hinglish | -0.79 [-5.56, 4.37] | no | no |
| E paired random-stock / all | -0.35 [-3.04, 2.34] | no | no |
| E paired random-stock / en | 8.94 [5.30, 12.91] | YES | YES |
| E paired random-stock / hi | -2.32 [-6.62, 1.66] | no | no |
| E paired random-stock / hinglish | -9.13 [-15.48, -2.78] | YES | YES |

### Claimed effects

- A paired med-orig / all: 18.11 [14.95, 21.26]
- A paired med-orig / en: 11.92 [7.62, 16.23]
- A paired med-orig / hi: 9.60 [4.64, 14.90]
- A paired med-orig / hinglish: 35.71 [28.97, 42.46]
- A paired med-ctrl / all: 16.36 [13.32, 19.39]
- A paired med-ctrl / en: 7.62 [2.98, 12.25]
- A paired med-ctrl / hi: 14.57 [9.60, 19.54]
- A paired med-ctrl / hinglish: 28.97 [22.62, 35.32]
- A paired ctrl-orig / hinglish: 6.75 [0.40, 13.10]
- B paired steer-med / all: -10.05 [-12.50, -7.59]
- B paired steer-med / en: -7.62 [-11.59, -3.64]
- B paired steer-med / hi: -13.58 [-17.88, -9.27]
- B paired steer-med / hinglish: -8.73 [-13.49, -4.37]
- B paired resta20-med / en: -8.94 [-13.25, -4.64]
- B paired cresta20-med / hi: -5.63 [-9.93, -1.66]
- C paired steer_nf4-med_nf4 / all: -11.68 [-14.25, -9.00]
- D paired steer_f16-med_f16 / all: -10.98 [-13.55, -8.41]
- D paired steer_f16-med_f16 / en: -8.61 [-12.58, -4.64]
- D paired steer_f16-med_f16 / hi: -14.24 [-18.54, -9.93]
- D paired steer_f16-med_f16 / hinglish: -9.92 [-14.68, -5.16]
- D paired steer_q4km-med_q4km / all: -12.15 [-15.07, -9.35]
- D paired steer_q4km-med_q4km / en: -11.26 [-15.56, -6.95]
- D paired steer_q4km-med_q4km / hi: -16.56 [-21.19, -11.92]
- D paired steer_q4km-med_q4km / hinglish: -7.94 [-13.89, -1.98]
- D paired steer_q3km-med_q3km / all: -11.10 [-13.79, -8.41]
- D paired steer_q3km-med_q3km / en: -9.93 [-13.91, -6.29]
- D paired steer_q3km-med_q3km / hi: -13.91 [-18.54, -9.27]
- D paired steer_q3km-med_q3km / hinglish: -9.13 [-14.68, -3.57]
- D paired steer_q4km-nopre-med_q4km-nopre / all: -9.35 [-11.92, -6.78]
- D paired steer_q4km-nopre-med_q4km-nopre / en: -6.29 [-10.26, -2.32]
- D paired steer_q4km-nopre-med_q4km-nopre / hi: -10.60 [-14.90, -6.29]
- D paired steer_q4km-nopre-med_q4km-nopre / hinglish: -11.51 [-16.27, -6.75]
- D paired steer_budget-phone-med_budget-phone / all: -8.64 [-11.10, -6.07]
- D paired steer_budget-phone-med_budget-phone / en: -6.95 [-10.93, -3.31]
- D paired steer_budget-phone-med_budget-phone / hi: -11.26 [-15.56, -6.95]
- D paired steer_budget-phone-med_budget-phone / hinglish: -7.54 [-12.70, -2.38]
- E paired protected-random / en: -6.29 [-10.60, -2.32]
- E paired protected-random / hinglish: 8.33 [2.38, 14.29]
- E paired random-stock / en: 8.94 [5.30, 12.91]
- E paired random-stock / hinglish: -9.13 [-15.48, -2.78]

### Fragile claim decisions (|diff| within 0.5 of 5, or a CI bound within 0.5 of 0)

- A paired ctrl-orig / hi: -4.97 [-8.94, -1.32] -> not claimed
- A paired ctrl-orig / hinglish: 6.75 [0.40, 13.10] -> claimed
- B paired resta20-med / all: -4.56 [-7.36, -1.64] -> not claimed
- C paired orig_nf4-orig / all: 4.56 [1.99, 7.13] -> not claimed
