# D8 tables: labelled RQ5 and RQ6 complete

| Setting | Medical ASR | Steered ASR | Change pp [95% CI] | R(s) [95% CI] | Clinical ORR med / steered |
|---|---:|---:|---|---|---|
| f16 | 36.8 | 25.8 | -10.98 [-13.55, -8.53] | F16 reference | 29.1 / 31.1 |
| q4km | 39.4 | 27.2 | -12.15 [-14.95, -9.23] | 1.11 [0.84, 1.44] | 27.1 / 32.7 |
| q3km | 39.0 | 27.9 | -11.10 [-13.79, -8.53] | 1.01 [0.74, 1.36] | 31.4 / 35.6 |
| q4km-nopre | 33.2 | 23.8 | -9.35 [-11.92, -6.78] | 0.85 [0.61, 1.16] | 25.5 / 31.7 |
| budget-phone | 34.8 | 26.2 | -8.64 [-11.21, -6.19] | 0.79 [0.54, 1.11] | 28.8 / 37.2 |

ASR denominator:856 harmful prompts/cell; ORR clinical306 benign twins/cell. All intervals pointwise; pooled ORR includes directional Hinglish. All pooled R intervals include1, so H5 is not supported, not proven false. RQ6: H6 is not supported. Pooled protection does not differ from stock or random; this is not equivalence.

Source core/deployment families retain their declared scopes. Conservative cross-family union is a sensitivity; original registration timing and omissions remain disclosed. All eight RQ6 tests are available; frozen Hinglish scores remain measurement-limited by the blind audit. Retention/NI intervals remain pointwise.


## RQ6: primary frozen-label contrasts

| Protected minus comparator | Language | Change pp [95% CI] | Raw bootstrap p | Deployment23 Holm p | Conservative58 Holm p |
|---|---|---|---:|---:|---:|
| stock | all | -0.35 [-2.57, +1.99] | 0.8130 | 1.0000 | 1.0000 |
| stock | en | +2.65 [-0.33, +5.96] | 0.1260 | 1.0000 | 1.0000 |
| stock | hi | -2.98 [-6.95, +0.66] | 0.1454 | 1.0000 | 1.0000 |
| stock | hinglish | -0.79 [-5.95, +4.37] | 0.8164 | 1.0000 | 1.0000 |
| random | all | +0.00 [-2.57, +2.57] | 1.0000 | 1.0000 | 1.0000 |
| random | en | -6.29 [-10.26, -2.32] | 0.0026 | 0.0468 | 0.0754 |
| random | hi | -0.66 [-4.30, +2.98] | 0.7742 | 1.0000 | 1.0000 |
| random | hinglish | +8.33 [+2.38, +14.29] | 0.0062 | 0.1054 | 0.1736 |

English protected minus random survives the 23-test deployment family, but not the conservative58-test sensitivity. Protected does not differ from stock in any primary stratum. Hinglish scores are retained as frozen judge outputs, not interpretable safety effects: the targeted blind audit overturned43/44 unsafe labels,39 involving degenerate text. This selected audit is not a replacement full-dataset estimate.

Protected raises clinical ORR versus stock by6.2pp pooled and13.7pp Hindi. These are supporting pointwise comparisons; pooled ORR includes directional Hinglish. Retention ratios for protected/random use unsteered stock medicalQ3, not unsteered variant counterparts.

Cross-check: all12 central ASR contrasts reproduced exactly using the central reference-ID order. Mac tables retain frozen dataset order; finite-bootstrap CIs and p-values differ slightly. See results/mac/nov11/rq6_handoff_verification.json.
