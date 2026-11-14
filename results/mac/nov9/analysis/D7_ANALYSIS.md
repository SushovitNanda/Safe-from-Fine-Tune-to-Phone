# D7: available within-Mac results

Five available Mac RQ5 contrasts x 2 metrics x 3 subsets x 4 languages; partial study family; not global confirmatory significance. Pointwise 95% paired bootstrap intervals; exact paired binary p-values. Hinglish ORR is directional. Do not treat partial-family correction as completed global Holm.

| Cell | ASR pooled | EN | HI | Hinglish | ORR general | ORR clinical |
|---|---:|---:|---:|---:|---:|---:|
| orig_q4km | 18.3 | 11.6 | 16.2 | 29.0 | 10.9 | 5.2 |
| orig_q4km-nopre | 19.7 | 12.6 | 15.9 | 32.9 | 18.0 | 6.5 |
| med_f16 | 36.8 | 24.8 | 27.5 | 62.3 | 22.0 | 29.1 |
| med_q4km | 39.4 | 28.1 | 30.1 | 63.9 | 20.2 | 27.1 |
| med_q3km | 39.0 | 20.2 | 31.8 | 70.2 | 25.8 | 31.4 |
| med_q4km-nopre | 33.2 | 19.2 | 24.2 | 60.7 | 17.3 | 25.5 |
| med_budget-phone | 34.8 | 16.9 | 26.5 | 66.3 | 22.9 | 28.8 |

## Pooled ASR contrasts

| Contrast | Difference (points) | Pointwise 95% CI | Partial-family Holm p |
|---|---:|---|---:|
| med_q4km minus med_f16 | +2.57 | [+0.23, +4.91] | 1 |
| med_q3km minus med_f16 | +2.22 | [-0.35, +4.79] | 1 |
| med_q4km-nopre minus med_q4km | -6.19 | [-8.76, -3.62] | 0.0004157 |
| med_budget-phone minus med_q3km | -4.21 | [-6.78, -1.75] | 0.1628 |
| orig_q4km-nopre minus orig_q4km | +1.40 | [-0.70, +3.50] | 1 |

## Interpretation

Medical Q4 no-preamble has lower ASR than medical Q4 official, contrary to the proposed preamble-removal worsening direction. Original no-preamble is higher in point estimate. Quantization effects are heterogeneous: inspect Hinglish separately rather than relying on pooled changes. These labels do not imply clinical utility or zero risk.

Original medical fidelity passed 50/50 centrally. The NEW steering gate has not passed by inheritance. GGUF repair retention: new Mac steered F16 gate/labels missing; Within-Mac difference-in-differences: original Mac F16 full cell missing; Protected-stock-random ASR: reported steered protected/random cells and labels missing; Actual clinic ROI: historical token-cap throughput is not useful-answer capacity.
