"""LaTeX tables for the thesis, generated from result files. Imported by build_thesis.py; each value in TABLES is a complete table environment."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def J(p): return json.load(open(ROOT / p, encoding="utf-8"))
D, S, F, V, K = J("results/drift/summary.json"), J("results/repair_test/summary.json"), J("results/final_stats/final.json"), J("results/final_stats/judge_validation.json"), J("results/judges/kappa.json")["kappa"]
BT = J("results/final_stats/bt_batch_check.json") if (ROOT / "results/final_stats/bt_batch_check.json").exists() else None
LS = ["all", "en", "hi", "hinglish"]; L3 = ["en", "hi", "hinglish"]
from decimal import Decimal, ROUND_HALF_UP
def hu(v, d=1):
    q = Decimal(1).scaleb(-d); r = Decimal(str(v)).quantize(q, rounding=ROUND_HALF_UP)
    return f"{r:+.{d}f}" if False else f"{r:.{d}f}"
def ci(x, k="ci95", d=1): return f"[{hu(x[k][0], d)}, {hu(x[k][1], d)}]"
def sg(v, d=1): return (("+" if v >= 0 else "") + hu(v, d)).replace("-", "$-$")
def dci(x, bold=True):
    t = f"{sg(x['diff'])} {ci(x)}".replace("[-", "[$-$").replace(", -", ", $-$")
    cl = x.get("claimed", bool(x.get("clear_of_zero") and x.get("ge5")))
    return r"\textbf{" + t + "}" if bold and cl else t
def tab(label, cap, cols, head, rows, size="scriptsize", wide=False):
    b = "\n".join(r for r in rows)
    return "\\begin{table}[tbp]\n\\centering\n\\caption{" + cap + "}\\label{" + label + "}\n\\" + size + "\n\\begin{adjustbox}{max width=\\linewidth}\n\\begin{tabular}{" + cols + "}\n\\toprule\n" + head + " \\\\\n\\midrule\n" + b + "\n\\bottomrule\n\\end{tabular}\n\\end{adjustbox}\n\\end{table}"
T = {}
# ---- platform
cp = F["cross_platform"]; rows = []
for n, c in cp.items():
    lab = {"med F16 Mac vs FP16 laptop": "Medical", "steer F16 Mac vs FP16 laptop": "Medical + vector"}[n]; a = c["paired_asr_a_minus_b"]
    rows.append(f"{lab} (full test, 1,612) & {100*c['same_safety_all']/c['n']:.1f}\\,\\% & {100*c['same_safety_harmful']/c['n_harmful']:.1f}\\,\\% & {100*c['same_refusal_all']/c['n']:.1f}\\,\\% & {c['asr_a']:.1f} / {c['asr_b']:.1f} & {dci(a, False)} \\\\")
T["platform"] = tab("tab:platform", "Mac (llama.cpp, F16 GGUF) against laptop (Transformers, FP16) on the same prompts. Agreement is on the judge's safety and refusal labels. ASR is pooled over 856 harmful prompts, Mac then laptop; the last column is the paired Mac minus laptop difference with 95\\,\\% interval.", "lrrrrr", "Model & Safety, all & Safety, harmful & Refusal, all & ASR Mac / laptop & Paired difference", rows)
# ---- kappa
def k(j, t, l): return K[f"{j}|{t}|{l}"]["kappa"]
rows = []
for n, j, t in (("Qwen3Guard, unsafe (primary)", "qwen3guard", "unsafe_primary"), ("Qwen3Guard, unsafe or controversial", "qwen3guard_sensitivity", "unsafe_primary"), ("WildGuard on back-translation, unsafe", "wildguard", "unsafe_primary"), ("Qwen3Guard, refusal", "qwen3guard", "refusal"), ("WildGuard on back-translation, refusal", "wildguard", "refusal")):
    rows.append(f"{n} & " + " & ".join(f"{k(j,t,l):.2f}" for l in L3) + f" & {k(j,t,'all'):.2f} \\\\")
T["kappa"] = tab("tab:kappa", "Cohen's $\\kappa$ of each judge against the 300 approved hand labels, on the original model's answers. Unsafe is scored on harmful prompts, refusal on all prompts. The pre-registered bar is 0.6, and the higher $\\kappa$ per language becomes the primary judge.", "lrrrr", "Judge and task & EN & HI & Hinglish & All", rows)
# ---- judge validation
m = V["medical_validation"]; rows = []
for l, n in (("en", "English"), ("hi", "Hindi"), ("hinglish", "Hinglish"), ("all", "Pooled")):
    x = m[l]; rows.append(f"{n} & {x['n_harmful']} & {x['agent_unsure_harmful']} & {x['primary_unsafe_among_agent_unsure']} & {x['n_scored']} & {x['agreement_primary_vs_agent']*100:.0f}\\,\\% & {x['kappa_primary_vs_agent']:.2f} & {x['kappa_refusal']:.2f} \\\\")
T["medval"] = tab("tab:medval", "Judges against a blind independent AI annotator on a stratified sample of the medical model's answers (40 harmful and 10 benign per language). ``Unreadable'' are answers the annotator could not classify; the next column counts how many of those the primary judge called unsafe. Agreement and $\\kappa$ exclude unreadable answers.", "lrrrrrrr", "Language & Harmful & Unreadable & Judged unsafe & Scored & Agreement & $\\kappa$ unsafe & $\\kappa$ refusal", rows)
# ---- RQ1
R = D["rq1"]; rows = [f"$G_{{\\mathrm{{HI}}}}$ (Hindi minus English) & {sg(R['gap|hi']['gap'])} & {ci(R['gap|hi'])} \\\\".replace("[-", "[$-$"), f"$G_{{\\mathrm{{Hinglish}}}}$ & {sg(R['gap|hinglish']['gap'])} & {ci(R['gap|hinglish'])} \\\\"]
for l, n in (("en", "English"), ("hi", "Hindi"), ("hinglish", "Hinglish"), ("all", "Pooled")):
    x = R[f"clinical_minus_general|{l}"]; rows.append(f"Clinical minus general, {n} & {sg(x['diff'])} & {ci(x)} \\\\".replace("[-", "[$-$"))
T["rq1"] = tab("tab:rq1", "The original model's gaps on test, in points of attack success, with 95\\,\\% bootstrap intervals.", "lrl", "Quantity & Value & Interval", rows)
# ---- rates
rows = []
for m_, n in (("orig", "Original"), ("ctrl", "Control"), ("med", "Medical"), ("orig_nf4", "Original NF4"), ("med_nf4", "Medical NF4")):
    r = D["rates"][m_]; rows.append(f"{n} & {r['asr|all|all']['rate']:.1f} {ci(r['asr|all|all'])} & " + " & ".join(f"{r[f'asr|all|{l}']['rate']:.1f}" for l in L3) + f" & {r['asr|general|all']['rate']:.1f} & {r['asr|clinical|all']['rate']:.1f} & {r['asr|all|all']['rate_sensitivity']:.1f} & {r['medmcqa_test500']:.1f} \\\\")
T["rates"] = tab("tab:rates", "Attack success on the 856 harmful test prompts (\\%), by language and harm type; sensitivity also counts Qwen3Guard's Controversial as unsafe. MedMCQA is test-500 accuracy.", "lrrrrrrrr".replace("rrrrrrrr", "lrrrrrrr"), "Model & Pooled & EN & HI & Hinglish & General & Clinical & Sens. & MedMCQA", rows)
# ---- RQ2
rows = []
Q = D["rq2"]
for n, key in (("Medical $-$ original", "med-orig"), ("Medical $-$ control", "med-ctrl"), ("Control $-$ original", "ctrl-orig")):
    for h in ("all", "general", "clinical"):
        rows.append(f"{n if h == 'all' else ''} & {h} & " + " & ".join(dci(Q[f"{key}|{h}|{l}"], True) for l in LS) + " \\\\")
T["rq2"] = tab("tab:rq2", "Paired differences in attack success on test (points, 95\\,\\% interval). Bold marks a claim under the pre-registered rule: at least 5 points with an interval clear of zero.", "llllll", "Comparison & Harm & Pooled & EN & HI & Hinglish", rows, size="scriptsize")
# ---- ORR
rows = []
for m_, n in (("orig", "Original"), ("ctrl", "Control"), ("med", "Medical"), ("orig_nf4", "Original NF4"), ("med_nf4", "Medical NF4")):
    r = D["rates"][m_]; rows.append(f"{n} & " + " & ".join(f"{r[f'orr|general|{l}']['rate']:.1f} / {r[f'orr|clinical|{l}']['rate']:.1f}" for l in LS) + " \\\\")
T["orr"] = tab("tab:orr", "Over-refusal on benign test prompts, general / clinical (\\%). Hinglish is directional only, because the refusal judge has $\\kappa = 0.31$ there.", "lrrrr", "Model & Pooled & EN & HI & Hinglish", rows)
# ---- degeneracy
dg = V["degeneracy"]; rows = []
for m_, n in (("original", "Original"), ("control", "Control"), ("medical", "Medical"), ("steering s0.5", "Steering 0.5"), ("ReSta a0.05", "ReSta 0.05")):
    rows.append(f"{n} & " + " & ".join(f"{dg[m_][l]['degenerate_pct']:.1f} & {dg[m_][l]['asr_all']:.1f} & {dg[m_][l]['asr_non_degenerate']:.1f}" for l in L3 + ["all"]) + " \\\\")
T["degen"] = tab("tab:degen", "Degenerate answers to harmful prompts (\\%, repetition loops or echo of the prompt, detected by a rule) and attack success over all answers and over non-degenerate answers only.", "lrrrrrrrrrrrr", " & \\multicolumn{3}{c}{English} & \\multicolumn{3}{c}{Hindi} & \\multicolumn{3}{c}{Hinglish} & \\multicolumn{3}{c}{Pooled} \\\\\nModel & Deg. & ASR & ASR non-deg. & Deg. & ASR & ASR non-deg. & Deg. & ASR & ASR non-deg. & Deg. & ASR & ASR non-deg.", rows, size="scriptsize")
nd = V["non_degenerate_paired"]; rows = []
for key, n in (("medical-original", "Medical $-$ original"), ("medical-control", "Medical $-$ control"), ("steering s0.5-medical", "Steering 0.5 $-$ medical")):
    rows.append(f"{n} & " + " & ".join(f"{sg(nd[f'{key}|{l}']['diff'])} {ci(nd[f'{key}|{l}'])} ($n$={nd[f'{key}|{l}']['n']})".replace("[-", "[$-$").replace(", -", ", $-$") for l in L3 + ["all"]) + " \\\\")
T["nondeg"] = tab("tab:nondeg", "Paired differences restricted to prompts where neither answer is degenerate (points, 95\\,\\% interval). This analysis was added after the audit and is exploratory.", "lllll", "Comparison & English & Hindi & Hinglish & Pooled", rows, size="scriptsize")
# ---- RQ3
o = J("handoff/D4_2026-11-08/overlap_jaccard.json"); j = o["jaccard_full_runs"]; f = o["split_half_floor"]; rows = []
g = lambda a, b: j[a].get(b, j[b].get(a))
names = {"en": "English", "hi": "Hindi", "hinglish": "Hinglish"}
for l in L3:
    oth = " / ".join("---" if m_ == l else f"{g(f'orig_{l}_eap-ig', f'orig_{m_}_eap-ig'):.2f}" for m_ in L3)
    rd = "at the floor; unstable" if l == "hinglish" else "no change beyond the floor"
    rows.append(f"{names[l]} & {g(f'orig_{l}_eap-ig', f'med_{l}_eap-ig'):.2f} & {f[f'orig_{l}_eap-ig']:.2f} / {f[f'med_{l}_eap-ig']:.2f} & {oth} & {rd} \\\\")
T["floors"] = tab("tab:floors", "Top-60 node overlap (Jaccard) between the original and medical circuits in each language, split-half noise floors, and overlap across languages for the original model.", "lrrrl", "Language & Orig.\\ vs med. & Floor orig.\\ / med. & vs EN / HI / Hinglish & Reading", rows)
rows = []
for l in L3:
    v_ = J(f"results/circuits/v2/validation_{l}.json")
    for i, kk in enumerate((20, 40, 60)):
        nmax = max(v_["necessity_drop"][f"rand{kk}_{r}"] for r in range(5)); smax = max(v_["sufficiency_recovery"][f"rand{kk}_{r}"] for r in range(5)); n = v_["necessity_drop"][f"top{kk}"]; s_ = v_["sufficiency_recovery"][f"top{kk}"]
        fn = lambda x, y: (r"\textbf{" + f"{x:.2f}" + "}" if x > y else f"{x:.2f}").replace("-", "$-$")
        rows.append(f"{names[l] if i == 0 else ''} & {kk} & {fn(n, nmax)} & {nmax:.2f} & {fn(s_, smax)} & {smax:.2f} \\\\")
T["valid"] = tab("tab:valid", "Validation with the preamble on (logits, 100 harmful dev prompts per language). Necessity is the drop in the refusal metric after mean-ablating the top-$k$ nodes in the original model. Sufficiency is its recovery after patching those nodes from the original into the medical model. Bold beats all five random sets. The gate is read at $k=40$.", "lrrrrr", "Language & $k$ & Necessity & max random & Sufficiency & max random", rows)
# ---- sweep
sw = J("results/repair_dev/sweep_table.json"); rows = []
nm = lambda n: n.replace("resta_a", "ReSta ").replace("cresta ReSta", "x").replace("steer_L", "Steer L").replace("_s", " s").replace("cReSta ", "Restr. ").replace("_top", " top")
for x in sorted(sw, key=lambda z: z["asr_all"]):
    p = x["p_mcnemar"]; ps = "--" if p is None else f"{p:.3f}"
    rows.append(f"{nm(x['name'])} & {x['asr_all']:.1f} & {sg(x['d_asr_vs_med'])} & " + "/".join(f"{x['asr'][l]:.0f}" for l in L3) + " & " + "/".join(f"{x['orr_general'][l]:.0f}" for l in L3) + " & " + "/".join(f"{x['orr_clinical'][l]:.0f}" for l in L3) + f" & {x['medmcqa']:.1f} ({sg(x['d_mq_vs_med'])}, {ps}) & {'yes' if x['A_prereg'] else 'no'} & {'yes' if x['C_orr_en_hi_vs_med'] else 'no'} \\\\")
T["sweep"] = tab("tab:sweep", "Every repair setting tried on the 360-prompt dev pass, sorted by pooled attack success (dev references: original 21.0, medical 35.7, MedMCQA medical 43.6). Language triples are EN/HI/Hinglish. ``Rule'' is the pre-registered selection rule; ``Am.~3'' is the trade-off rule defined after the sweep.", "lrrlllrll".replace("lrrlllrll", "lrrlllrcc"), "Setting & ASR & vs med. & ASR by lang. & ORR gen. & ORR clin. & MedMCQA ($\\Delta$, $p$) & Rule & Am.~3", rows, size="scriptsize")
# ---- RQ4
names4 = [("ReSta a0.05", "ReSta 0.05 (primary, out of grid)"), ("Steer L24 s0.5", "Steering L24 0.5 (primary)"), ("ReSta a0.10", "ReSta 0.10"), ("ReSta a0.20", "ReSta 0.20"), ("Restricted a0.25 top20", "Restricted 0.25, top 20\\,\\%"), ("Steer L24 s1.0", "Steering L24 1.0")]
rows = [f"Original & {S['asr']['Original']['all']['rate']:.1f} & {S['asr']['Original']['en']['rate']:.1f} & {S['asr']['Original']['hi']['rate']:.1f} & {S['asr']['Original']['hinglish']['rate']:.1f} & -- & {S['orr']['Original']['general|all']['rate']:.1f} / {S['orr']['Original']['clinical|all']['rate']:.1f} & {S['medmcqa']['Original']['accuracy']:.1f} \\\\",
        f"Medical & {S['asr']['Medical']['all']['rate']:.1f} & {S['asr']['Medical']['en']['rate']:.1f} & {S['asr']['Medical']['hi']['rate']:.1f} & {S['asr']['Medical']['hinglish']['rate']:.1f} & -- & {S['orr']['Medical']['general|all']['rate']:.1f} / {S['orr']['Medical']['clinical|all']['rate']:.1f} & {S['medmcqa']['Medical']['accuracy']:.1f} \\\\", "\\midrule"]
for k_, n in names4:
    if k_ not in S["asr"]: continue
    a = S["asr"][k_]; rows.append(f"{n} & {a['all']['rate']:.1f} & {a['en']['rate']:.1f} & {a['hi']['rate']:.1f} & {a['hinglish']['rate']:.1f} & {dci(S['vs_med'][k_]['all'])} & {S['orr'][k_]['general|all']['rate']:.1f} / {S['orr'][k_]['clinical|all']['rate']:.1f} & {S['medmcqa'][k_]['accuracy']:.1f} \\\\")
if "cr20" in F.get("extra_cells", {}):
    e = F["extra_cells"]["cr20"]; rows.append(f"Restricted 0.20, top 20\\,\\% (late) & {e['asr']['all']['rate']:.1f} & {e['asr']['en']['rate']:.1f} & {e['asr']['hi']['rate']:.1f} & {e['asr']['hinglish']['rate']:.1f} & {dci(e['vs_med']['all'])} & -- & {e['medmcqa']['acc']:.1f} \\\\")
T["rq4"] = tab("tab:rq4", "Repair test cells at FP16: attack success (\\%, 856 harmful prompts), paired difference from the medical model (points), over-refusal general / clinical (\\%, pooled; Hinglish directional) and MedMCQA test-500. Settings were fixed on dev before generation, except the last row.", "lrrrrlrr", "Model & ASR & EN & HI & Hinglish & vs medical & ORR & MedMCQA", rows)
rows = []
for k_, n in names4:
    if k_ not in S["vs_med"]: continue
    rows.append(f"{n} & " + " & ".join(dci(S["vs_med"][k_][l]) for l in LS) + " \\\\")
T["rq4lang"] = tab("tab:rq4lang", "Repair minus medical on test by language (points, 95\\,\\% interval; bold is a claim under the pre-registered rule).", "lllll", "Repair & Pooled & EN & HI & Hinglish", rows, size="scriptsize")
# ---- NF4
rows = []; Q5 = D["rq5_nf4"]
for l, n in (("en", "English"), ("hi", "Hindi"), ("hinglish", "Hinglish"), ("all", "Pooled")):
    fm = lambda x: f"{sg(x['loss'])} {ci(x)}".replace("[-", "[$-$").replace(", -", ", $-$")
    v_ = lambda x: "non-inferior" if x["non_inferior"] else ("inferior" if x["inferior"] else "inconclusive")
    d_ = Q5[f"deltadelta|{l}"]; rows.append(f"{n} & {fm(Q5[f'nf4_loss|orig|{l}'])} {v_(Q5[f'nf4_loss|orig|{l}'])} & {fm(Q5[f'nf4_loss|med|{l}'])} {v_(Q5[f'nf4_loss|med|{l}'])} & {sg(d_['dd'])} {ci(d_)} \\\\".replace("[-", "[$-$").replace(", -", ", $-$"))
T["nf4"] = tab("tab:nf4", "NF4 minus FP16 attack success (points, 95\\,\\% interval, non-inferiority verdict at a 5-point margin; inconclusive: the interval neither clears zero nor stays under 5) and the difference-in-differences.", "llll", "Language & Original & Medical & $\\Delta\\Delta$(NF4)", rows, size="scriptsize")
rows = []
for k_, n in (("Steer L24 s0.5", "Steering 0.5"), ("ReSta a0.05", "ReSta 0.05")):
    for l in LS:
        x = S["nf4"][k_][l]; r = x["retention"]; rs = f"{hu(r['R'], 2)} [{hu(r['ci95'][0], 2)}, {hu(r['ci95'][1], 2)}]" if r["R"] is not None else f"undefined ({hu(r['denominator'])} pt)".replace("-", "$-$")
        rows.append(f"{n if l == 'all' else ''} & {dict(all='Pooled', en='EN', hi='HI', hinglish='Hinglish')[l]} & {x['asr_med_fp16']:.1f} & {x['asr_rep_fp16']:.1f} & {x['asr_med_nf4']:.1f} & {x['asr_rep_nf4']:.1f} & {rs} & {'yes' if x['non_inferior'] else 'no'} \\\\")
T["ret"] = tab("tab:ret", "NF4 retention on the laptop: retention of the repair at NF4 against FP16. $R$ is undefined when the FP16 effect is below 5 points.", "llrrrrlc", "Repair & Lang. & Med FP16 & Rep FP16 & Med NF4 & Rep NF4 & $R$(NF4) & Non-inf.", rows)
# ---- GGUF
if "gguf" in F:
    G = F["gguf"]; N = {"f16": "F16", "q4km": "Q4\\_K\\_M", "q3km": "Q3\\_K\\_M", "q4km-nopre": "Q4\\_K\\_M, no preamble", "budget-phone": "Budget-phone"}; rows = []
    for s, n in N.items():
        if s not in G["rates"]: continue
        rows.append(f"{n} & {G['rates'][s]['med']['all']['rate']:.1f} & {G['rates'][s]['steer']['all']['rate']:.1f} & " + " & ".join(dci(G["steer_effect"][s][l]) for l in LS) + " \\\\")
    T["gguf"] = tab("tab:gguf", "Mac GGUF cells: pooled attack success of the medical model without and with the steering vector (\\%), and the paired effect of the vector by language (points, 95\\,\\% interval; bold is a claim).", "lrrllll", "Setting & Med. & +vector & Pooled & EN & HI & Hinglish", rows, size="scriptsize")
    rows = []
    for s, n in N.items():
        if s == "f16" or s not in G["retention"]: continue
        def rr(l):
            r = G["retention"][s][l]; return f"{hu(r['R'], 2)} [{hu(r['ci95'][0], 2)}, {hu(r['ci95'][1], 2)}]".replace("[-", "[$-$").replace(", -", ", $-$") if r["R"] is not None else f"undef.\\ ({r['denominator']:.1f})".replace("-", "$-$")
        l_ = G["loss_steered"][s]["all"]; lm = G["loss_medical"][s]["all"]
        rows.append(f"{n} & " + " & ".join(rr(l) for l in LS) + f" & {dci(l_, False)} {'NI' if l_['non_inferior'] else 'not NI'} & {dci(lm, False)} {'NI' if lm['non_inferior'] else 'not NI'} \\\\")
    T["retention"] = tab("tab:retention", "GGUF retention on the Mac: retention $R(s)$ of the steering effect at each GGUF setting, relative to the Mac F16 cells, and the pooled attack-success loss against F16 for the steered and the unsteered medical model (NI: non-inferior at a 5-point margin).", "lllllll", "Setting & $R$ pooled & $R$ EN & $R$ HI & $R$ Hinglish & Loss, steered & Loss, medical", rows, size="scriptsize")
    rows = []
    for n, d_ in (("Medical, Q4\\_K\\_M", G["no_preamble"].get("med")), ("Medical + vector, Q4\\_K\\_M", G["no_preamble"].get("steer")), ("Original, Q4\\_K\\_M", G["no_preamble"].get("orig"))):
        if d_: rows.append(f"Removing the preamble: {n} & " + " & ".join(dci(d_[l]) for l in LS) + " \\\\")
    lm = G["last_mile"]
    rows.append("Last mile: medical, phone $-$ F16 & " + " & ".join(dci(lm["medical_vs_mac_f16"][l]) for l in LS) + " \\\\"); rows.append("Last mile: medical + vector, phone $-$ F16 & " + " & ".join(dci(lm["steered_vs_mac_f16"][l]) for l in LS) + " \\\\")
    for s, n in (("q4km", "Q4\\_K\\_M"), ("q4km-nopre", "Q4\\_K\\_M, no preamble")): rows.append(f"$\\Delta\\Delta$, {n} & " + " & ".join(dci(G["deltadelta"][s][l]) for l in LS) + " \\\\")
    T["lastmile"] = tab("tab:lastmile", "Preamble removal, last-mile gap and difference-in-differences on GGUF (points, 95\\,\\% interval; bold is a claim). $\\Delta\\Delta$ uses the laptop FP16 cells as the FP16 reference, because no original Mac F16 cell exists.", "lllll", "Contrast & Pooled & EN & HI & Hinglish", rows, size="scriptsize")
if F["rq6"].get("available"):
    R6 = F["rq6"]; rows = []
    for k_, n in (("stock", "Stock"), ("protected", "Protected"), ("random", "Random")): rows.append(f"{n} & " + " & ".join(f"{R6['rates'][k_][l]['rate']:.1f}" for l in LS) + " \\\\")
    for k_, n in (("protected_minus_stock", "Protected $-$ stock"), ("protected_minus_random", "Protected $-$ random"), ("random_minus_stock", "Random $-$ stock")): rows.append(f"{n} & " + " & ".join(dci(R6[k_][l]) for l in LS) + " \\\\")
    if "retention" in R6:
        rows.append(r"Retention $R$, stock / protected / random & \multicolumn{4}{l}{" +" / ".join(f"{hu(R6['retention'][k_]['all']['R'], 2)} [{hu(R6['retention'][k_]['all']['ci95'][0], 2)}, {hu(R6['retention'][k_]['all']['ci95'][1], 2)}]" if R6['retention'][k_]['all'].get('R') is not None else "n/a" for k_ in ("stock", "protected", "random")) + "} \\\\")
    for b, n in (("general", "general"), ("clinical", "clinical")):
        o = R6["orr"][f"{b}|all"]; rows.append(f"ORR {n}, stock / protected / random & \\multicolumn{{4}}{{l}}{{{o['stock']['rate']:.1f} / {o['protected']['rate']:.1f} / {o['random']['rate']:.1f}; protected $-$ random {dci(o['protected_minus_random'], False)}}} \\\\")
    T["rq6"] = tab("tab:rq6", r"RQ6 on the Mac at Q3\_K\_M with the steering vector attached: attack success (\%), paired differences (points, 95\,\% interval; bold is a claim), pooled retention and pooled over-refusal (\%).", "lllll", "Build & Pooled & EN & HI & Hinglish", rows, size="scriptsize")
# ---- RQ6 ORR per language
if F["rq6"].get("available"):
    rows = []; LN6 = {"en": "EN", "hi": "HI", "hinglish": "Hinglish", "all": "Pooled", "general": "General", "clinical": "Clinical"}
    for b in ("general", "clinical"):
        for l in LS:
            o = F["rq6"]["orr"][f"{b}|{l}"]
            rows.append(f"{LN6[b]} & {LN6[l]} & {o['stock']['rate']:.1f} & {o['protected']['rate']:.1f} & {o['random']['rate']:.1f} & {dci(o['protected_minus_stock'])} & {dci(o['protected_minus_random'])} \\\\")
    T["rq6orr"] = tab("tab:rq6orr", r"RQ6 over-refusal (\%) on benign prompts per language, with paired differences (points, 95\,\% interval; bold is a claim). Hinglish is directional only.", "llrrrll", "Set & Language & Stock & Protected & Random & Protected $-$ stock & Protected $-$ random", rows, size="scriptsize")
# ---- 58-test union (Mac lane, D8 evidence)
D8 = ROOT / "reports/D8/d8_evidence.json"
if D8.exists():
    U = J("reports/D8/d8_evidence.json").get("complete_union_including_rq6_holm", {})
    if U:
        rows = [f"{k.replace('_', ' ').replace(':', ': ').replace(' hinglish', ' Hinglish')} & {v:.4f} & {'yes' if v < 0.05 else 'no'} \\\\" for k, v in sorted(U.items(), key=lambda kv: kv[1])]
        T["union58"] = tab("tab:union58", f"Holm-adjusted $p$ over the conservative union of all {len(U)} declared tests (second author's computation from the central labels, Mac row order).", "lrc", "Test & Adjusted $p$ & Rejected", rows, size="scriptsize")
# ---- Holm
h = F["holm_combined"]["tests"]; nr = [k_ for k_, x in h.items() if not x["reject"]]; rows = []
for k_, x in sorted(h.items(), key=lambda kv: kv[1]["p"]):
    rows.append(f"{k_.replace('_', ' ').replace(' hinglish', ' Hinglish')} & {x['p']:.4f} & {'yes' if x['reject'] else 'no'} \\\\")
T["holm"] = tab("tab:holm", f"One combined Holm family over all {F['holm_combined']['m']} tests declared in the pre-registration ($\\alpha=0.05$; $p$ from the paired bootstrap, exact McNemar for MedMCQA). The analyses as first run used separate families.", "lrc", "Test & $p$ & Rejected", rows, size="scriptsize")
TABLES = T
if __name__ == "__main__":
    print(sorted(T))
