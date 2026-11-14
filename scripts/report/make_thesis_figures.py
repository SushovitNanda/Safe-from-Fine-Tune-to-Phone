"""All thesis figures as PNG in Report/figures/, drawn from result files only.

    python scripts/report/make_thesis_figures.py
"""
import json, os, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Report/figures"; OUT.mkdir(parents=True, exist_ok=True)
# validated categorical palette (scripts in the dataviz skill): fixed order, colour follows the entity
BLUE, ORANGE, AQUA, YELLOW, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#6250d6"
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "xtick.major.size": 2.5, "ytick.major.size": 2.5, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False, "legend.frameon": False, "legend.fontsize": 7,
                     "axes.titlesize": 8, "axes.titleweight": "bold", "axes.titlecolor": INK, "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.04})
LANG = {"en": "English", "hi": "Hindi", "hinglish": "Hinglish", "all": "Pooled"}
LS = ["all", "en", "hi", "hinglish"]
def J(p): return json.load(open(ROOT / p, encoding="utf-8"))
def grid(ax, axis="y"):
    ax.grid(True, axis=axis, color=GRID, lw=0.5); ax.set_axisbelow(True)
def save(fig, name):
    fig.savefig(OUT / f"{name}.png"); plt.close(fig); print("wrote", name)
def bars(ax, groups, series, colors, values, errs=None, width=0.8, labels=False):
    n = len(series); w = width / n; x = np.arange(len(groups))
    for j, (s, c) in enumerate(zip(series, colors)):
        pos = x + (j - (n - 1) / 2) * w
        y = [values[g][s] for g in groups]
        yerr = None
        if errs: yerr = np.array([[y[i] - errs[g][s][0], errs[g][s][1] - y[i]] for i, g in enumerate(groups)]).T
        ax.bar(pos, y, w * 0.86, color=c, label=s, zorder=2)
        if yerr is not None: ax.errorbar(pos, y, yerr=yerr, fmt="none", ecolor=INK, elinewidth=0.6, capsize=1.3, capthick=0.6, zorder=3)
        if labels:
            for p, v_ in zip(pos, y): ax.text(p, v_ + 1, f"{v_:.0f}", ha="center", va="bottom", fontsize=5.5, color=MUTED)
    ax.set_xticks(x); ax.set_xticklabels(groups)

def box(ax, x, y, w, h, title, sub=None, fc="#eef4fc", ec=BLUE, fs=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.015", fc=fc, ec=ec, lw=0.8))
    if sub:
        ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=fs - 1.3, color=MUTED, linespacing=1.15)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.15)
def arrow(ax, a, b, label=None, off=(0, 0.018), rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=9, lw=0.9, color=MUTED, connectionstyle=f"arc3,rad={rad}"))
    if label: ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], label, ha="center", va="bottom", fontsize=5.4, color=MUTED, linespacing=1.1)
def canvas(w, h):
    f, a = plt.subplots(figsize=(w, h)); a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off"); return f, a

# ---- diagrams
def fig_chain():
    f, a = canvas(4.8, 2.2)
    t = [("RQ1  Gap", "weaker refusal in Hindi,\nHinglish, clinical harm?"), ("RQ2  Drift", "does benign medical\nfine-tuning widen it?"), ("RQ3  Cause", "which components\ncarry refusal?"),
         ("RQ4  Fix", "can it be repaired\nwithout retraining?"), ("RQ5  Last mile", "does the repair survive\nquantization?"), ("RQ6  Protection", "do the circuit's tensors\nmerit more bits?")]
    w, h = 0.285, 0.38; xs = [0.02, 0.3575, 0.695]; ys = [0.58, 0.04]
    pos = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[2], ys[0]), (xs[2], ys[1]), (xs[1], ys[1]), (xs[0], ys[1])]
    for (x, y), (ti, s_) in zip(pos, t): box(a, x, y, w, h, ti, s_, fs=7)
    arrow(a, (xs[0] + w, ys[0] + h / 2), (xs[1], ys[0] + h / 2)); arrow(a, (xs[1] + w, ys[0] + h / 2), (xs[2], ys[0] + h / 2))
    arrow(a, (xs[2] + w / 2, ys[0]), (xs[2] + w / 2, ys[1] + h)); arrow(a, (xs[2], ys[1] + h / 2), (xs[1] + w, ys[1] + h / 2)); arrow(a, (xs[1], ys[1] + h / 2), (xs[0] + w, ys[1] + h / 2))
    a.text(xs[2] + w / 2 + 0.012, (ys[0] + ys[1] + h) / 2, "tensor map", ha="left", va="center", fontsize=5.8, color=MUTED)
    save(f, "fig_rq_chain")
def fig_pipeline():
    f, a = canvas(4.8, 3.0); h = 0.2; fs = 6.2
    box(a, 0.01, 0.76, 0.205, h, "Data package", "sets, twins, leak checks", fs=fs); box(a, 0.262, 0.76, 0.205, h, "Fine-tuning", "LoRA medical, control", fs=fs)
    box(a, 0.514, 0.76, 0.205, h, "Merged FP16", "per-tensor hashes", fs=fs); box(a, 0.766, 0.76, 0.205, h, "Circuits", "EAP-IG, ablation", fs=fs)
    box(a, 0.262, 0.42, 0.335, h, "Laptop lane, RTX 4080", "FP16, NF4, repairs, 1,612 prompts", fc="#eef9f4", ec=AQUA, fs=fs)
    box(a, 0.64, 0.42, 0.35, h, "Mac lane, llama.cpp Metal", "F16, Q4_K_M, Q3_K_M, no preamble", fc="#fdf1ea", ec=ORANGE, fs=fs)
    box(a, 0.262, 0.06, 0.33, h, "One judge host", "Qwen3Guard, and WildGuard on\nback-translated Hindi", fc="#f3f1fc", ec=VIOLET, fs=fs)
    box(a, 0.64, 0.06, 0.35, h, "Statistics", "paired bootstrap, McNemar,\nHolm, retention", fc="#f3f1fc", ec=VIOLET, fs=fs)
    for x0, x1 in ((0.215, 0.262), (0.467, 0.514), (0.719, 0.766)): arrow(a, (x0, 0.86), (x1, 0.86))
    arrow(a, (0.58, 0.76), (0.46, 0.62)); arrow(a, (0.67, 0.76), (0.8, 0.62)); arrow(a, (0.44, 0.42), (0.44, 0.26)); arrow(a, (0.78, 0.42), (0.55, 0.26)); arrow(a, (0.592, 0.16), (0.64, 0.16))
    box(a, 0.01, 0.22, 0.225, 0.4, "Rules", "pre-registration\nand amendments;\ndev for choosing,\ntest for reporting", fc="#f5f5f2", ec=MUTED, fs=fs)
    a.text(0.81, 0.33, "ZIPs of answers", fontsize=5.6, color=MUTED, ha="center")
    save(f, "fig_pipeline")
def fig_toc():
    f, a = canvas(4.8, 2.5); w, h = 0.205, 0.42; fs = 6.4
    z = [("Inputs", "open small model,\nmultilingual sets,\nno retraining budget"), ("Activities", "measure, fine-tune,\nlocate, repair,\nquantize, protect"), ("Outputs", "per-language rates,\nvalidated vector,\nprotected GGUF"), ("Outcome", "clinics deploy with\na measured safety\nloss and a fix")]
    x = [0.01, 0.262, 0.514, 0.766]
    for xi, (ti, s_) in zip(x, z): box(a, xi, 0.54, w, h, ti, s_, fs=fs)
    for i in range(3): arrow(a, (x[i] + w, 0.75), (x[i + 1], 0.75))
    box(a, 0.01, 0.03, 0.98, 0.38, "Assumptions that must hold", "judges read each language and each model's outputs correctly; dev settings transfer to test;\nlaptop and Mac agree; fine-tuned answers are meaningful, not degenerate;\ndeployers will adopt a run-time vector", fc="#fdf6e6", ec=YELLOW, fs=fs)
    arrow(a, (0.3645, 0.41), (0.3645, 0.54))
    save(f, "fig_theory_of_change")

# ---- training
def fig_loss():
    f, ax = plt.subplots(figsize=(3.4, 1.8))
    for n, c, lab in (("med", BLUE, "Medical"), ("ctrl", ORANGE, "Control")):
        d = J(f"models/runs/{n}/train_summary.json")["loss_curve"]
        if isinstance(d[0], dict):
            k = [x for x in d[0] if "step" in x][0]; l = [x for x in d[0] if "loss" in x][0]; xs, ys = [e[k] for e in d], [e[l] for e in d]
        else:
            xs, ys = zip(*d) if isinstance(d[0], (list, tuple)) else (range(len(d)), d)
        ax.plot(xs, ys, color=c, lw=1.3, label=lab)
        ax.text(list(xs)[-1] + 4, list(ys)[-1], lab, color=INK, fontsize=6.5, va="center")
    ax.set_xlabel("Optimizer step"); ax.set_ylabel("Loss on assistant tokens"); ax.legend(loc="upper right", ncol=2); grid(ax); save(f, "fig_loss")

# ---- RQ1, RQ2
D = J("results/drift/summary.json")
def r_(m, h, l): return D["rates"][m][f"asr|{h}|{l}"]
def fig_rq1():
    f, ax = plt.subplots(figsize=(3.6, 2.0)); G = ["English", "Hindi", "Hinglish", "Pooled"]; K = ["en", "hi", "hinglish", "all"]
    vals = {g: {"General harm": r_("orig", "general", k)["rate"], "Clinical harm": r_("orig", "clinical", k)["rate"]} for g, k in zip(G, K)}
    errs = {g: {"General harm": r_("orig", "general", k)["ci95"], "Clinical harm": r_("orig", "clinical", k)["ci95"]} for g, k in zip(G, K)}
    bars(ax, G, ["General harm", "Clinical harm"], [BLUE, ORANGE], vals, errs, labels=False); ax.set_ylabel("Attack success (%)"); ax.legend(loc="upper left", ncol=2); ax.set_ylim(0, 58); grid(ax); save(f, "fig_rq1_gap")
def fig_rq2():
    f, ax = plt.subplots(figsize=(4.4, 2.1)); G = ["English", "Hindi", "Hinglish", "Pooled"]; K = ["en", "hi", "hinglish", "all"]; M = [("orig", "Original", BLUE), ("ctrl", "Control", ORANGE), ("med", "Medical", AQUA)]
    vals = {g: {n: r_(m, "all", k)["rate"] for m, n, _ in M} for g, k in zip(G, K)}; errs = {g: {n: r_(m, "all", k)["ci95"] for m, n, _ in M} for g, k in zip(G, K)}
    bars(ax, G, [n for _, n, _ in M], [c for *_, c in M], vals, errs, labels=False); ax.set_ylabel("Attack success (%)"); ax.legend(loc="upper left", ncol=3); ax.set_ylim(0, 82); grid(ax); save(f, "fig_rq2_drift")
def forest(ax, rows, xlabel, colors=None, zero=True):
    y = np.arange(len(rows))[::-1]
    for yi, (lab, d, lo, hi, *rest) in zip(y, rows):
        c = rest[0] if rest else BLUE
        ax.plot([lo, hi], [yi, yi], color=c, lw=1.1, zorder=2); ax.plot(d, yi, "o", ms=3.8, color=c, mec=SURF, mew=0.5, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows]); ax.set_xlabel(xlabel)
    if zero: ax.axvline(0, color=MUTED, lw=0.7)
    grid(ax, "x"); ax.tick_params(axis="y", length=0)
def fig_rq2_harm():
    f, axs = plt.subplots(1, 2, figsize=(4.8, 1.9), sharey=True)
    for ax, (h, t) in zip(axs, (("general", "General harm"), ("clinical", "Clinical harm"))):
        rows = []
        for n, c in (("med-orig", BLUE), ("med-ctrl", ORANGE)):
            for l in LS:
                x = D["rq2"][f"{n}|{h}|{l}"]; rows.append((f"{ 'vs original' if n == 'med-orig' else 'vs control'}, {LANG[l]}", x["diff"], x["ci95"][0], x["ci95"][1], c))
        forest(ax, rows, "Medical minus reference (points)"); ax.set_title(t); ax.set_xlim(-5, 52)
    save(f, "fig_rq2_harm")
def fig_orr():
    f, axs = plt.subplots(1, 2, figsize=(4.8, 1.8), sharey=True); K = ["en", "hi", "hinglish"]; G = ["English", "Hindi", "Hinglish"]; M = [("orig", "Original", BLUE), ("ctrl", "Control", ORANGE), ("med", "Medical", AQUA)]
    for ax, (b, t) in zip(axs, (("general", "General benign"), ("clinical", "Clinical benign"))):
        vals = {g: {n: D["rates"][m][f"orr|{b}|{k}"]["rate"] for m, n, _ in M} for g, k in zip(G, K)}; errs = {g: {n: D["rates"][m][f"orr|{b}|{k}"]["ci95"] for m, n, _ in M} for g, k in zip(G, K)}
        bars(ax, G, [n for _, n, _ in M], [c for *_, c in M], vals, errs); ax.set_title(t); grid(ax); ax.set_ylim(0, 80)
    axs[0].set_ylabel("Over-refusal (%)"); axs[0].legend(loc="upper left", ncol=1); save(f, "fig_orr")
def fig_degen():
    V = J("results/final_stats/judge_validation.json")["degeneracy"]; f, axs = plt.subplots(1, 2, figsize=(4.8, 1.9)); M = [("original", "Original", BLUE), ("control", "Control", ORANGE), ("medical", "Medical", AQUA)]; K = ["en", "hi", "hinglish"]; G = ["English", "Hindi", "Hinglish"]
    vals = {g: {n: V[m][k]["degenerate_pct"] for m, n, _ in M} for g, k in zip(G, K)}; bars(axs[0], G, [n for _, n, _ in M], [c for *_, c in M], vals, labels=True); axs[0].set_ylabel("Degenerate answers to harmful prompts (%)"); axs[0].legend(loc="upper left"); axs[0].set_ylim(0, 80); grid(axs[0]); axs[0].set_title("Degenerate text")
    vals = {g: {"All answers": V["medical"][k]["asr_all"], "Non-degenerate": V["medical"][k]["asr_non_degenerate"]} for g, k in zip(G, K)}; bars(axs[1], G, ["All answers", "Non-degenerate"], [AQUA, VIOLET], vals, labels=True); axs[1].set_ylabel("Medical attack success (%)"); axs[1].legend(loc="upper left"); axs[1].set_ylim(0, 80); grid(axs[1]); axs[1].set_title("Effect on the medical model")
    f.tight_layout(); save(f, "fig_degeneracy")

# ---- RQ3
def fig_rq3():
    f, axs = plt.subplots(2, 3, figsize=(4.8, 2.7), sharex=True); ks = [20, 40, 60]
    for j, l in enumerate(("en", "hi", "hinglish")):
        V = J(f"results/circuits/v2/validation_{l}.json")
        for i, (key, ti) in enumerate((("necessity_drop", "Necessity"), ("sufficiency_recovery", "Sufficiency"))):
            ax = axs[i, j]; d = V[key]; top = [d[f"top{k}"] for k in ks]; rnd = [[d[f"rand{k}_{r}"] for r in range(5)] for k in ks]; x = np.arange(3)
            for xi, rs in zip(x, rnd): ax.plot([xi + 0.14] * 5, rs, "o", ms=2.2, color=ORANGE, zorder=2, alpha=0.9)
            ax.plot(x - 0.14, top, "o", ms=4.2, color=BLUE, zorder=3); ax.axhline(0, color=MUTED, lw=0.6); ax.set_xticks(x); ax.set_xticklabels([f"k={k}" for k in ks]); grid(ax)
            if j == 0: ax.set_ylabel(f"{ti}\n(logits)")
            if i == 0: ax.set_title(LANG[l])
    axs[0, 0].plot([], [], "o", ms=4.2, color=BLUE, label="Top-k circuit"); axs[0, 0].plot([], [], "o", ms=2.2, color=ORANGE, label="Random sets"); axs[0, 0].legend(loc="lower right", handletextpad=0.1, borderpad=0)
    f.tight_layout(pad=0.4); save(f, "fig_rq3_validation")
def fig_jacc():
    o = J("handoff/D4_2026-11-08/overlap_jaccard.json"); J_ = o["jaccard_full_runs"]; n = ["orig_en_eap-ig", "orig_hi_eap-ig", "orig_hinglish_eap-ig", "med_en_eap-ig", "med_hi_eap-ig", "med_hinglish_eap-ig"]; lab = ["Orig EN", "Orig HI", "Orig Hg", "Med EN", "Med HI", "Med Hg"]
    M = np.array([[1.0 if a == b else J_[a].get(b, J_[b].get(a, np.nan)) for b in n] for a in n]); f, ax = plt.subplots(figsize=(2.8, 2.5))
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list("seq", ["#f2f7fd", "#a9caf0", BLUE, "#123d73"]); im = ax.imshow(M, cmap=cm, vmin=0, vmax=1)
    ax.set_xticks(range(6)); ax.set_xticklabels(lab, rotation=45, ha="right"); ax.set_yticks(range(6)); ax.set_yticklabels(lab); ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    for i in range(6):
        for j in range(6):
            if i != j: ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6, color=(SURF if M[i, j] > 0.55 else INK))
    save(f, "fig_rq3_jaccard")

# ---- RQ4
def fig_sweep():
    rows = {}
    for l in open(ROOT / "results/repair_dev/sweep.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r.get("resta") is not None or r.get("steer"): rows[r["name"]] = r
    def m(r): return "Steering" if r.get("steer") else ("Restricted ReSta" if r.get("resta_tensors") else "Whole-model ReSta")
    B = {json.loads(l)["name"]: json.loads(l) for l in open(ROOT / "results/repair_dev/baselines_v2.jsonl", encoding="utf-8")}
    f, axs = plt.subplots(1, 2, figsize=(4.8, 2.25), sharex=True); col = {"Whole-model ReSta": BLUE, "Restricted ReSta": ORANGE, "Steering": AQUA}; mk = {"Whole-model ReSta": "o", "Restricted ReSta": "s", "Steering": "^"}
    for r in rows.values():
        if r["asr|all"] > 55: continue
        k = m(r); axs[0].plot(r["asr|all"], r["medmcqa_dev1000"], mk[k], ms=4.2, color=col[k], mec=SURF, mew=0.4); axs[1].plot(r["asr|all"], r["orr_clinical|all"], mk[k], ms=4.2, color=col[k], mec=SURF, mew=0.4)
    med = B["baseline_med"]; orig = B["baseline_orig"]; mqm = J("results/cells/dev_pass__med__fp16/medmcqa_dev1000.json")["accuracy"] * 100; mqo = J("results/cells/dev_pass__orig__fp16/medmcqa_dev1000.json")["accuracy"] * 100
    axs[0].axhline(mqm, color=MUTED, lw=0.7, ls="--"); axs[0].text(40, mqm + 0.2, "medical", fontsize=5.8, color=MUTED, ha="right", va="bottom"); axs[0].axvline(orig["asr|all"], color=MUTED, lw=0.7, ls=":"); axs[0].axvline(med["asr|all"], color=MUTED, lw=0.7, ls="--")
    axs[1].axhline(med["orr_clinical|all"], color=MUTED, lw=0.7, ls="--"); axs[1].axhline(orig["orr_clinical|all"], color=MUTED, lw=0.7, ls=":"); axs[1].axvline(orig["asr|all"], color=MUTED, lw=0.7, ls=":"); axs[1].axvline(med["asr|all"], color=MUTED, lw=0.7, ls="--")
    axs[0].set_ylabel("MedMCQA dev-995 (%)"); axs[1].set_ylabel("Clinical over-refusal (%)")
    for a in axs: a.set_xlabel("Pooled attack success on dev (%)"); grid(a, "both")
    h = [plt.Line2D([], [], marker=mk[k], ls="", color=col[k], ms=4.2, label=k) for k in col] + [plt.Line2D([], [], ls="--", color=MUTED, lw=0.7, label="medical"), plt.Line2D([], [], ls=":", color=MUTED, lw=0.7, label="original")]
    f.legend(handles=h, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.07), columnspacing=0.9, handletextpad=0.25); f.tight_layout(pad=0.3); save(f, "fig_rq4_sweep")
def fig_forest():
    S = J("results/repair_test/summary.json"); order = ["Steer L24 s1.0", "Steer L24 s0.5", "ReSta a0.20", "ReSta a0.10", "ReSta a0.05", "Restricted a0.25 top20"]; name = {"Steer L24 s1.0": "Steering 1.0", "Steer L24 s0.5": "Steering 0.5", "ReSta a0.20": "ReSta 0.20", "ReSta a0.10": "ReSta 0.10", "ReSta a0.05": "ReSta 0.05", "Restricted a0.25 top20": "Restricted 0.25"}
    order = [o for o in order if o in S["vs_med"]]; f, axs = plt.subplots(1, 4, figsize=(4.8, 1.9), sharey=True)
    for ax, l in zip(axs, LS):
        rows = [(name[o], S["vs_med"][o][l]["diff"], *S["vs_med"][o][l]["ci95"], AQUA if o.startswith("Steer") else BLUE if o.startswith("ReSta") else ORANGE) for o in order]; forest(ax, rows, ""); ax.set_title(LANG[l]); ax.set_xlim(-34, 12); ax.axvline(-5, color=GRID, lw=0.6, ls="--")
    f.supxlabel("Repair minus medical, attack success", fontsize=7, y=-0.04); f.tight_layout(pad=0.3); save(f, "fig_rq4_forest")

# ---- RQ5, platform
F = J("results/final_stats/final.json")
def fig_rq5():
    if "gguf" not in F: print("skip rq5"); return
    G = F["gguf"]["rates"]; S_ = ["f16", "q4km", "q3km", "q4km-nopre", "budget-phone"]; N_ = ["F16", "Q4", "Q3", "Q4\nno pre.", "Phone"]; S_ = [s for s in S_ if s in G]
    f, axs = plt.subplots(1, 4, figsize=(4.8, 2.0), sharey=False)
    for ax, l in zip(axs, LS):
        for key, c, n in (("med", AQUA, "Medical"), ("steer", VIOLET, "Medical + vector")):
            y = [G[s][key][l]["rate"] for s in S_]; lo = [G[s][key][l]["ci95"][0] for s in S_]; hi = [G[s][key][l]["ci95"][1] for s in S_]; x = np.arange(len(S_))
            ax.fill_between(x, lo, hi, color=c, alpha=0.14, lw=0); ax.plot(x, y, "-o", color=c, lw=1.2, ms=2.8, label=n)
        ax.set_xticks(np.arange(len(S_))); ax.set_xticklabels(N_[:len(S_)], fontsize=5.3); ax.set_title(LANG[l]); grid(ax)
    axs[0].set_ylabel("Attack success (%)"); h, lab = axs[0].get_legend_handles_labels(); f.legend(h, lab, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.0), fontsize=6); f.tight_layout(pad=0.3, rect=(0, 0, 1, 0.88)); save(f, "fig_rq5_gguf")
def fig_platform():
    M = J("results/mac_judged/summary.json")["cells"]; L = D["rates"]; f, ax = plt.subplots(figsize=(2.6, 2.4)); pts = []
    for key, m_, l_ in (("asr", "mac__med_f16", "med"),):
        for h, h2 in (("pooled", "all"), ("harmful_general", "general"), ("harmful_clinical", "clinical")):
            for l in ("en", "hi", "hinglish"):
                pts.append((L[l_][f"asr|{h2}|{l}"]["rate"], M[m_][f"asr|{h}|{l}"]["rate"]))
    x, y = zip(*pts); ax.plot([0, 75], [0, 75], color=MUTED, lw=0.7); ax.plot(x, y, "o", ms=4.2, color=BLUE, mec=SURF, mew=0.4); ax.set_xlabel("Laptop FP16 attack success (%)"); ax.set_ylabel("Mac F16 attack success (%)"); ax.set_xlim(0, 75); ax.set_ylim(0, 75); grid(ax, "both"); save(f, "fig_platform")

for fn in (fig_chain, fig_pipeline, fig_toc, fig_loss, fig_rq1, fig_rq2, fig_rq2_harm, fig_orr, fig_degen, fig_rq3, fig_jacc, fig_sweep, fig_forest, fig_rq5, fig_platform):
    try: fn()
    except Exception as e:
        import traceback; print("FAILED", fn.__name__, repr(e)); traceback.print_exc(limit=2)
