"""Assemble Report/main.tex from scripts/report/thesis_src/*.tex, inlining generated tables, the abstract and the related-work draft.

    python scripts/report/build_thesis.py
Placeholders: %%TABLE:name%%, %%ABSTRACT%%, %%RELATED%%, %%CR20%%. Citation keys are mapped by thesis_src/citekeys.json when present.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from thesis_tables import TABLES, F

SRC = ROOT / "scripts/report/thesis_src"
s = "\n".join(p.read_text(encoding="utf-8") for p in sorted(SRC.glob("[0-9]*.tex")))
ab = (SRC / "abstract.txt").read_text(encoding="utf-8").strip() if (SRC / "abstract.txt").exists() else "Abstract pending."
plain = re.sub(r"\\textbf\{([^}]*)\}", r"\1", ab); plain = re.sub(r"\\[a-zA-Z]+|[{}$~]", " ", plain)
n = len(plain.split()); print("abstract words:", n); assert n <= 250, f"abstract is {n} words"
s = s.replace("%%ABSTRACT%%", ab)
ex = (SRC / "exec_summary.tex").read_text(encoding="utf-8") if (SRC / "exec_summary.tex").exists() else ""
s = s.replace("%%EXEC%%", ex)
rw = ROOT / "Report/drafts/related_work.tex"
rt = re.sub(r"\\section\{Related Work\}\s*(\\label\{[^}]*\})?\s*", "", rw.read_text(encoding="utf-8")) if rw.exists() else "Pending."
s = s.replace("%%RELATED%%", rt)
c = ""
if "cr20" in F.get("extra_cells", {}):
    e = F["extra_cells"]["cr20"]["vs_med"]["all"]
    h = F["extra_cells"]["cr20"]["vs_med"]["hi"]; q = F["extra_cells"]["cr20"]["medmcqa"]
    c = (f"The best restricted setting on dev, $\\alpha=0.20$, was also run on test after the test results were known. It gives ${e['diff']:+.1f}$ $[{e['ci95'][0]:.1f}, {e['ci95'][1]:.1f}]$ pooled, not a measurable repair. Only Hindi moves by at least 5 points (${h['diff']:+.1f}$ $[{h['ci95'][0]:.1f}, {h['ci95'][1]:.1f}]$), and MedMCQA is {q['acc']:.1f}" + r"\,\% against 45.0\,\%.")
s = s.replace("%%CR20%%", c)
BTP = ROOT / "results/final_stats/bt_batch_check.json"
if BTP.exists():
    b = json.load(open(BTP, encoding="utf-8"))
    same = "stayed at " + f"{b['asr_hi_batch8']:.1f}" if b['asr_hi_batch8'] == b['asr_hi_batch16'] else f"moved from {b['asr_hi_batch8']:.1f} to {b['asr_hi_batch16']:.1f}"
    bt = (f"Re-translating the medical cell's {b['n_hindi']} Hindi answers at batch 16 left {b['verdict_identical']} of {b['n_hindi']} WildGuard verdicts unchanged, and Hindi attack success {same}" + r"\,\%, so the batch size does not affect the labels of that cell.")
else:
    bt = "A check that re-translates the medical cell at batch 16 was started and did not finish, so the effect is unquantified."
s = s.replace("%%BT%%", bt)
R6 = F["rq6"]
if R6.get("available"):
    pr, ps, rs = (R6[k]["all"] for k in ("protected_minus_random", "protected_minus_stock", "random_minus_stock"))
    rt = {k: R6["rates"][k]["all"]["rate"] for k in ("stock", "protected", "random")}
    from decimal import Decimal, ROUND_HALF_UP
    def hu(v, d=1): return f"{Decimal(str(v)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP):.{d}f}"
    f = lambda x: f"${'+' if x['diff'] >= 0 else ''}{hu(x['diff'])}$ $[{hu(x['ci95'][0])}, {hu(x['ci95'][1])}]$"
    LN = {"en": "English", "hi": "Hindi", "hinglish": "Hinglish"}
    CN = {"protected_minus_random": "protected minus random", "protected_minus_stock": "protected minus stock"}
    NW = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
    cl = [(c, l) for c in ("protected_minus_random", "protected_minus_stock") for l in LN if R6[c][l]["claimed"]]
    hd = F.get("holm_deployment_with_rq6")
    nfam = hd["m"] if hd else 23
    clt = (f"{NW.get(len(cl), len(cl))} per-language difference{'s' if len(cl) != 1 else ''} meet{'s' if len(cl) == 1 else ''} the claim rule: " + "; ".join(f"in {LN[l]}, {CN[c]} is {f(R6[c][l])}" for c, l in cl) + ". ") if cl else "No per-language difference meets the claim rule (at least 5 points with the interval clear of zero). "
    ps_cl = [l for l in LN if R6["protected_minus_stock"][l]["claimed"]]; rs_cl = [l for l in LN if R6["random_minus_stock"][l]["claimed"]]
    cost_t = ""
    if cl and not ps_cl and rs_cl:
        oc_ps = R6["orr"]["clinical|all"]["protected_minus_stock"]; oc_hi = R6["orr"]["clinical|hi"]["protected_minus_stock"]
        clt += (f"We read {'both' if len(cl) == 2 else 'these'} as movement of the one random draw, not as an effect of protection. Protected minus stock is not clear of zero in any language (the intervals reach about 6 to 7 points, so equivalence is not shown either), while random minus stock is "
                + " and ".join(f"{f(R6['random_minus_stock'][l])} in {LN[l]}" for l in rs_cl) + f". The English protected-minus-random contrast meets the H6 criterion on its own, and it is the only one of the 8 RQ6 tests that survives Holm correction when they are added, as pre-registered, to the deployment family ({nfam} tests; adjusted $p = 0.047$). In the second author's conservative 58-test union of all declared tests it does not survive (adjusted $p = 0.075$). It is not support for H6: protected is no safer than stock in English, and one draw cannot show that random allocation behaves this way in general. The Hinglish contrasts are a judge artefact on degenerate text (blind audit below). ")
        cost_t = f"Protection raises clinical over-refusal: {f(oc_ps)} points above stock pooled and {f(oc_hi)} in Hindi, both meeting the claim rule. "
    ret = R6.get("retention", {})
    rtt = ""
    if ret and all(ret[k]["all"].get("R") is not None for k in ("stock", "protected", "random")):
        rtt = "Retention against the Mac F16 gain is " + f"{ret['stock']['all']['R']:.2f} for stock, {ret['protected']['all']['R']:.2f} for protected and {ret['random']['all']['R']:.2f} for random" + ", with overlapping intervals. "
    oc = R6["orr"]["clinical|all"]; og = R6["orr"]["general|all"]
    ort = (rf"Pooled over-refusal for stock, protected and random is {oc['stock']['rate']:.1f}, {oc['protected']['rate']:.1f} and {oc['random']['rate']:.1f}\,\% on clinical prompts and {og['stock']['rate']:.1f}, {og['protected']['rate']:.1f} and {og['random']['rate']:.1f}\,\% on general prompts (per-language figures in Table~\ref{{tab:rq6orr}}). ")
    lim_t = r"Two further limits: the random draw shares one upgraded tensor with the protected set, and no unsteered protected or random cell was generated, so retention for these builds uses the unsteered stock cell as its reference and measures steered attack success rather than retained repair."
    opener = "Protection made no measurable difference. " if not pr["clear_of_zero"] else ""
    sup = R6["H6_supported"]
    if sup: vt = r"H6 is supported: the circuit-protected build keeps the repair better than the matched random build by at least 5 points, with one random draw as the control."
    elif pr["ci95"][1] < 0: vt = r"H6 is not supported by the claim rule. The protected build is measurably safer than the matched random build, but by less than the 5-point margin."
    elif pr["ci95"][0] > 0: vt = r"H6 is not supported. The protected build is measurably \emph{less} safe than the matched random build."
    else: vt = r"H6 is not supported. In our one draw, giving the circuit's tensors more bits did not keep the repair measurably better than spending the same bits on random tensors."
    r6 = (r"\paragraph{How the cells were produced.} The Mac lane registered the test pair before generating it, ran the corrected protected and random Q3\_K\_M builds with the same steering vector, preamble, stop rule and 1,612 test prompts as the stock steered cell, and both cells passed validation with no errors. The laptop judged them with the same conventions as every other cell."
          + "\n\n%%TABLE:rq6%%\n\n"
          + r"\paragraph{Result.} " + opener + "With the vector attached, pooled attack success is " + rf"{rt['stock']:.1f}\,\% for stock, {rt['protected']:.1f}\,\% for protected and {rt['random']:.1f}\,\% for random (Table~\ref{{tab:rq6}}, Fig.~\ref{{fig:rq6}}). "
          + f"Protected minus random is {f(pr)} points, protected minus stock {f(ps)} and random minus stock {f(rs)}. " + rtt.rstrip()
          + "\n\n" + r"\paragraph{Per-language contrasts.} " + clt.rstrip()
          + "\n\n" + r"\paragraph{Cost and limits.} " + cost_t + ort + lim_t
          + "\n\n" + r"\paragraph{Verdict.} " + vt + r" RQ5 had already shown that stock Q3\_K\_M keeps the repair, so there was little loss to recover, and RQ3 could not link the map to the drift. The control is a single random draw, so tensor-selection variance is not covered.")
    r6d = (r"Protection beat a matched random allocation of the same bits by the margin, though with one random draw." if sup else
           r"Protection did not beat a matched random allocation of the same bits by the margin (Section~\ref{sec:rq6}).")
else:
    r6 = (r"\paragraph{Status.} The protected and random builds are complete and checked (Section~\ref{sec:exp}): both files are 1,797,062,144 bytes against 1,799,740,928 for stock, every unselected tensor is byte-identical to stock, and both passed a 100-prompt operational check with no errors. "
          r"The test cells for the protected and random builds with the steering vector attached had not been generated when this report was written, so \textbf{RQ6 is not answered here}. "
          r"RQ5 already sets the bar that protection has to clear. Stock Q3\_K\_M keeps the steering effect (retention 1.01, interval 0.74 to 1.36), so there is little loss for protection to recover. Because the circuit map did not explain the drift, we expect protection and the random control to perform alike. That is a prediction, not a result.")
    r6d = r"RQ6 is not yet answered. Because stock Q3\_K\_M already keeps the repair, protection has little to recover."
c5 = (r"\item An equal-size protection test for GGUF with a matched random control." if R6.get("available")
      else r"\item An equal-size protection design for GGUF with a matched random control, built and checked; its safety test is pending.")
s = s.replace("%%C5%%", c5)
s = s.replace("%%RQ6DISC%%", r6d)
s = s.replace("%%RQ6%%", r6)
MV = ROOT / "results/review_final/majority_vote.json"
a6 = a1 = ""
if MV.exists():
    M = json.load(open(MV, encoding="utf-8"))
    if "rq6_sample" in M:
        q = M["rq6_sample"]; e, h = q["en"], q["hinglish"]
        a6 = (r"\paragraph{Blind audit of the labels.} Because the per-language contrasts rest on judge labels, two further blind readers labelled a sample of " + f"{q['n']} answers: for each language, both builds' answers to 30 prompts where the builds' verdicts differed and 10 where they agreed, shuffled, without the judge's labels. The two readers agreed with each other on {q['auditors_agree_with_each_other']} of {q['n']}. "
              + f"In English the majority of judge and readers kept the judge's label on {e['judge_equals_majority']} of {e['n']} answers, overturned {e['judge_unsafe_overturned']} of its {e['judge_unsafe']} unsafe labels ({e['judge_unsafe_overturned_and_degenerate']} of them degenerate text), and the direction of the discordant pairs survived: the random build was the unsafe one in {e['discordant_pairs']['majority'].get('random_unsafe_only', 0)} of 30 pairs and the protected build in {e['discordant_pairs']['majority'].get('protected_unsafe_only', 0)}. "
              + f"In Hinglish the readers overturned {h['judge_unsafe_overturned']} of the judge's {h['judge_unsafe']} unsafe labels, {h['judge_unsafe_marked_degenerate_by_both']} of which both readers marked as degenerate, leaving {h['discordant_pairs']['majority'].get('neither_unsafe', 0)} of the 30 discordant pairs with neither answer unsafe. "
              + r"The Hinglish per-language RQ6 differences are therefore mostly a judge artefact on degenerate text and are not interpreted; the English difference between the random build and stock is supported by the readers. The sample over-represents discordant prompts, so it cannot estimate pooled rates; under the readers the random build stays the less safe one in English (17 against 5 unsafe answers of 40 each) and the Hinglish difference disappears (1 against 0). The pooled verdict, that protection is no better than random, rests on the full-cell labels and is not reversed by the audit; if anything, the audit removes the one language in which protected looked worse than random.")
    if "hand_labels" in M:
        hl = M["hand_labels"]; k = hl["by_kind"]
        a1 = (f" A final blind third reading of all 300 items (one agent per language) gives a majority vote over the approved labels, the second annotator and the third reading: {k.get('unanimous', 0)} unanimous, {k.get('approved_in_majority', 0)} with the approved label in the majority, {k.get('approved_outvoted', 0)} where the approved label was outvoted and {k.get('three_way_split', 0)} three-way splits. "
              + ("The judge chosen for each language is the same under the majority labels as under the approved labels. " if hl["judge_choice_unchanged"] else r"\textbf{Under the majority labels the judge choice changes for at least one language.} ")
              + "The approved labels remain the frozen primary labels; the majority vote is reported as the final consistency check.")
s = s.replace("%%AUDIT6%%", a6).replace("%%AUDIT1%%", a1)
miss = []
def tb(m):
    k = m.group(1)
    if k not in TABLES: miss.append(k); return ""
    return TABLES[k]
s = re.sub(r"%%TABLE:([a-z0-9_]+)%%", tb, s)
keys = SRC / "citekeys.json"
if keys.exists():
    mp = json.load(open(keys, encoding="utf-8"))
    def cite(m): return r"\cite{" + ",".join(mp.get(x.strip(), x.strip()) for x in m.group(1).split(",")) + "}"
    s = re.sub(r"\\cite\{([^}]*)\}", cite, s)
s = re.sub(r"[ \t]+\n", "\n", s)
(ROOT / "Report/main.tex").write_text(s, encoding="utf-8")
print("written; missing tables:", miss, "; chars", len(s))
