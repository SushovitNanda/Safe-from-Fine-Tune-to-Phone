"""Compile final centrally labelled RQ5/RQ6 LaTeX report."""
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2]
BUNDLE='https://data1b.fullyjustified.net/tlextras-2022.0r0.tar'


def main():
    data=json.loads((ROOT/'reports/D8/d8_evidence.json').read_text());roi=json.loads((ROOT/'results/mac/nov11/roi_evidence.json').read_text())
    pre=(ROOT/'reports/research_report.template.tex').read_text().split('\\begin{document}')[0]
    pre=pre.replace('MAC EXPERIMENT REPORT','D8 | RQ5-RQ6 HANDOFF').replace('Safe from Fine-Tune to Phone: Mac Experiment Report','Mac RQ5-RQ6 Research Handoff').replace('November 4-5 execution, findings, limitations and blockers','D8 final deployment and protection results, numeric parity and conditional ROI').replace(r'\fontsize{10.5}{13}\selectfont',r'\fontsize{10.2}{12.5}\selectfont')
    rows=[]
    names={'f16':'F16','q4km':r'Q4\_K\_M','q3km':r'Q3\_K\_M','q4km-nopre':'Q4, no preamble','budget-phone':'Budget-phone'}
    for r in data['rq5_rows']:
        rows.append(f"{names[r['setting']]} & {r['medical_ASR']:.1f} & {r['steered_ASR']:.1f} & {r['steering_difference_pp']:+.2f} & [{r['steering_ci95'][0]:+.2f}, {r['steering_ci95'][1]:+.2f}]\\\\")
    table='\n'.join(rows)
    rq6_rows=[]
    for key,r in data['rq6_tests'].items():
        comp='Stock' if r['b']=='rep_steer_q3km' else 'Random'
        lang={'all':'Pooled','en':'English','hi':'Hindi','hinglish':'Hinglish*'}[r['lang']]
        rq6_rows.append(f"{comp} & {lang} & {r['difference_pp']:+.2f} & [{r['ci95_pp'][0]:+.2f}, {r['ci95_pp'][1]:+.2f}] & {data['deployment23_Mac_order_holm'][key]:.4f}"+r"\\")
    rq6_table='\n'.join(rq6_rows)
    numeric=[]
    for tag in ['med','ctrl']:
        s=json.loads((ROOT/f'results/mac/nov11/d2_{tag}_numeric.json').read_text())
        for n,v in s['different_tensors'].items():
            parts=n.split('.');label=f"{tag} L{parts[2]} {parts[-2].replace('_',r'\_')}"
            numeric.append(f"{label} & {v['max_abs_diff']:.8g} & {v['n_elements_different']}\\\\")
    numeric='\n'.join(numeric)
    text=r'''\begin{document}
{\sffamily\bfseries\fontsize{23}{27}\selectfont\color{Ink}Safe from Fine-Tune to Phone\par}
{\sffamily\large\color{Accent}Mac research results and D8 handoff\par}
{\small\color{Muted}Manish | Prepared 11 November 2026 | Branch: manishshaw-handoff-v3-complete\par}
\vspace{6pt}
\textbf{Status.} All five full steered deployment cells are complete and centrally labelled (8,060 responses). Their ZIPs match the judge's import hashes. Both corrected M19 cells are complete and centrally labelled (3,224 responses). This final D8 analysis includes all eight RQ6 primary tests: circuit protection shows no pooled safety benefit against stock or matched random. H5 and H6 are not supported.

\section{RQ5: steering lowers attack success across settings}
Each cell has 856 harmful prompts and 756 benign prompts across English, Hindi and Hinglish. ASR below is a percentage of deliberately harmful test prompts, not clinical incident prevalence. Effects are steered minus medical, in percentage points; intervals are pointwise paired bootstrap (10,000 resamples, seed13).
\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}lrrrr@{}}
\toprule
Setting & Medical ASR & Steered ASR & Change & 95\% interval\\
\midrule
TABLE
\bottomrule
\end{tabular*}
All five pooled steering effects survive the supplied deployment-family Holm correction. Absolute safety is not established: residual ASR and over-refusal remain high. The intervention is an unchanged layer24/strength0.5 control vector on existing medical GGUFs, not repaired weight files.

\begin{center}\includegraphics[width=.98\linewidth]{../../reports/D8/figures/rq5_asr_languages.png}\end{center}
{\footnotesize\color{Muted}Central D7 primary judges: English/Hinglish Qwen3Guard; Hindi WildGuard after IndicTrans2. Intervals here are pointwise. Source labels and raw-run fingerprints are joined by prompt ID.\par}

\newpage
\section{Retention and the cost of over-refusal}
\begin{center}\includegraphics[width=.96\linewidth]{../../reports/D8/figures/rq5_retention.png}\end{center}
Pooled $R(s)$ is 1.11 for Q4, 1.01 for Q3, 0.85 without the preamble and 0.79 for the phone stack. Every pooled interval contains1: the predicted loss of retention is \textbf{not supported}, rather than proven absent. Language intervals are also wide. Ratios use the \emph{Mac} medical/steered F16 gain as denominator, with a five-point observed-gain floor. Nonpositive resampled denominators are counted; ratio intervals are not silently conditioned on dropping them.

\begin{center}\includegraphics[width=.98\linewidth]{../../reports/D8/figures/rq5_overrefusal.png}\end{center}
Clinical ORR increases by 1.96 points at F16, 5.56 at Q4, 4.25 at Q3, 6.21 without the preamble and 8.50 on the phone stack. Pooled ORR includes Hinglish, whose refusal agreement is weak; Hinglish-specific ORR is directional. These trade-offs matter even where ASR improves. Laptop MedMCQA is45.0\% medical versus45.4\% steering; this shared-weight benchmark does not validate clinical care.

Pointwise quantization noninferiority must be distinguished from a five-point difference claim. Medical pooled Q4/Q3 loss upper bounds are4.91/4.79 points, but no Q4 language row passes; Q3 fails Hindi/Hinglish. Steered Q3 pooled loss is2.10 points with upper4.79, while Hinglish is$+8.73$ with upper15.08. Pooled summaries therefore do not establish uniform multilingual preservation.

\newpage
\section{RQ6: no demonstrated pooled protection benefit}
The steered Q3 stock/protected/random pooled ASR is 27.9/27.6/27.6\%. Protected-minus-random is 0.00 points and protected-minus-stock is $-0.35$; both intervals include zero. \textbf{H6 is not supported}; this does not establish equivalence or clinical safety.

\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}llrrr@{}}
\toprule
Protected minus & Stratum & Change pp & Pointwise 95\% CI & Holm $p$ (23)\\
\midrule
RQ6ROWS
\bottomrule
\end{tabular*}
{\footnotesize *Frozen Hinglish judge outputs are retained for reproducibility, but the blind audit identifies these apparent safety contrasts as a judge artefact on degenerate text. Do not interpret them as safety effects.\par}

\begin{center}\includegraphics[width=.98\linewidth]{../../reports/D8/figures/rq6_protection.png}\end{center}
English protected-minus-random is $-6.29$ points and survives the 23-test deployment family, but not the conservative 58-test union sensitivity. Protected does not differ from stock in any primary stratum; English random-minus-stock is $+8.94$ points. This supports a weakness of this single random build, not a demonstrated improvement over stock.

Protected raises clinical ORR versus stock by 6.2 points pooled and 13.7 in Hindi (supporting pointwise comparisons). Pooled clinical ORR is 35.6/41.8/40.5\% for stock/protected/random and includes directional Hinglish. Pooled joint-gain ratios are 1.01/1.04/1.04: protected/random use the unsteered \emph{stock} baseline, not unsteered counterpart builds.

The targeted blind audit overturned 43/44 judge-unsafe Hinglish answers, 39 involving degenerate text. Its selected sample is not a replacement full-dataset estimate. Frozen primary labels remain unchanged. All 12 supplied central ASR contrasts reproduce exactly using the central reference-ID order. Tables here preserve frozen Mac dataset order, explaining small finite-bootstrap differences in intervals and $p$ values. Audit sources: \path{handoff/D7_2026-11-11/README.md} and \path{results/review_final/majority_vote.json}.

\newpage
\section{RQ6 construction and numerical reproducibility}
D4 uses original-model normalized absolute EAP-IG scores summed over languages. Attention and FFN matrices share family-level scores. G3a passes clearly in Hinglish and marginally in English at$k=40$, not Hindi there; original/medical circuit overlap is not distinguishable from split-half noise within language. The map does not explain the observed safety drift.

Review corrected a real confound: layer0 FFN zeros represented excluded attribution, not low importance. V2 excludes those tensors from all protected and random candidate pools. Eight Q8\_0 upgrades are kept, with a deterministic tie at the eighth matrix,19 Q2\_K donors and seed13 shape/type/transition matching. Both files are1,797,062,144 bytes versus stock1,799,740,928; they are equal and within1\%. All expected types/shapes/metadata and263 byte-identical unselected tensors were verified. Both corrected models passed100/100 fixed calibration checks before test generation. V1 remains historical, not a reported RQ6 artifact.

M19 compares corrected protected and matched-random Q3, \emph{both with the same vector}, against the already-labelled stock steeredQ3. The primary protected-minus-stock and protected-minus-random tests cover pooled and three language strata. One random draw remains a limitation; prompt bootstrap does not measure tensor-selection variance. Both central label sets are now imported and verified against delivered ZIP hashes, prompt IDs, run fingerprints, stop settings and token counts. The matched comparisons do not demonstrate a pooled protection benefit.

\section{Merge reproducibility: the numeric dependency is resolved}
The other285 medical and284 control tensors match the laptop's raw F16 hashes. Each listed differing tensor contains exactly one different element; every difference is one directional F16 nextafter step. Maximum differences are$3.81\times10^{-6}$ medical and$1.53\times10^{-5}$ control. These are consistent with a rounding-path difference, without proving its cause or asserting exact checkpoint identity.
\begin{center}\begin{tabular}{lrr}
\toprule
Tensor abbreviation & Max absolute difference & Elements different\\
\midrule
NUMERIC
\bottomrule
\end{tabular}\end{center}
Full names, shapes, means, element counts and verified reference hashes are in \path{results/mac/nov11/d2_med_numeric.json} and \path{d2_ctrl_numeric.json}. D4's31 producer checksums and the eight SFT byte mismatches are accounted for by CRLF/LF conversion; raw local and producer hashes remain distinct.

\newpage
\section{Cost method: measured throughput, conditional economics}
Only the new EOS/EOT-stopped runs are used for timing; old capped timings are excluded. SteeredQ3 processes0.603 evaluation requests/s at eight slots, including prefill. This is \emph{not} useful-answer clinic capacity or single-user latency. The benchmark has adversarial prompts, capped answers and degenerate outputs.
\begin{center}\includegraphics[width=.97\linewidth]{../../reports/D8/figures/roi_conditional_scenario.png}\end{center}
At a hypothetical10,000 requests/month, the example local budget is\$13.57/month versus\$3.60 at numerically matched API token budgets: no local saving in that scenario. Conditional break-even is37,681 requests, above the32,575-request evaluation-based capacity budget at30 hours/month and50\% utilization. The apparent higher-volume break-even is therefore outside that fixed local capacity assumption.

API input/output prices are the official listed\$0.40/\$1.60 per million tokens for \href{https://developers.openai.com/api/docs/models/gpt-4.1-mini}{GPT-4.1 mini}, checked11 November; the page marks it deprecated, so it is a reference-price illustration, not a procurement recommendation. Hardware\$600,36-month amortization,50\% allocation,40W power,\$0.20/kWh,\$5 monthly overhead and clinic demand are \emph{assumed}. API tokenization, billing/quality equivalence, measured power and actual clinic traffic were not established. The calculator provides sensitivity arithmetic, not measured clinic ROI or a spending recommendation.

\section{Research limitations and remaining handoff}
A reproduced post-hoc heuristic flags28.7\% of medicalF16 harmful answers and64.7\% in Hinglish as repetitions/echoes/short outputs. It includes potentially valid short refusals, is not human quality adjudication, and does not replace primary ASR. G4 failed as written; dev trade-offs were amended post hoc, ReSta0.05 was outside the grid, and the deployment-method switch was test-informed. The source study's original registration timing cannot be proven, as its own corrections disclose; new Mac protocols preserve their recorded prospective commits.

The phone stack is emulated on the Mac; physical-phone performance was not measured. Within-Mac difference-in-differences is unavailable without original MacF16. Supplied laptop-reference DID is only a mixed-engine sensitivity. Phone-minus-F16, no-preamble-minus-official and phone-minus-Q3 remain separately named. Incoming core35/deployment15 families retain their source scopes; the prospective eight RQ6 tests extend the deployment family, and the complete conservative58-test union is reported as a sensitivity. The English RQ6 comparison survives the23-test deployment family but not that wider union. Retention/NI intervals are pointwise.

\textbf{Completion:} M19 generation, M20 analysis, conditional M21 economics and M22/D8 are complete. No central-label dependency remains. M23 model/submission publication is prepared and awaits the team\textquotesingle s public go-ahead. Public release uses a fresh redacted artifact, not the private working repository. Upstream Tiny Aya CC-BY-NC-4.0 conditions are retained; no public upload has been performed.
\end{document}
'''
    # Avoid accidental word/number concatenation in the readable prose.
    import re
    text=re.sub(r'\b(seed|contains|is|are|with|and|by|at|medical|steered|stock|overhead|checked|hours|passed|models|verified|upgrades|donors|versus|within|other|upper|hypothetical|processes|the|conservative|original|core|deployment|prospective|above|budget|flags|F16|layer)(?=\d)',r'\1 ',text)
    text=text.replace('strength0.5','strength 0.5').replace('are4.91','are 4.91').replace('flags28.7','flags 28.7').replace('supplied35','supplied 35')
    text=text.replace('medicalF16','medical F16').replace('medicalF 16','medical F16').replace('SteeredQ3','Steered Q3').replace('steeredQ3','steered Q3').replace('steeredQ 3','steered Q3').replace("'s31","'s 31").replace('matrix,19','matrix, 19').replace(r'\$600,36',r'\$600, 36').replace('amortization,50','amortization, 50').replace('allocation,40W','allocation, 40 W').replace('power,\\$0.20',r'power, \$0.20').replace('kWh,\\$5',r'kWh, \$5')
    text=re.sub(r'(?<=[A-Za-z])(?=\\\$)', ' ', text)
    text=re.sub(r'(?<=[A-Za-z])(?=\$)', ' ', text)
    text=text.replace('at$k','at $k').replace('intervals are4','intervals are 4').replace('MacF16','Mac F16').replace('30 hours','30 hours')
    text=text.replace('RQ6ROWS',rq6_table).replace('TABLE',table).replace('NUMERIC',numeric)
    tex=ROOT/'output/pdf/manish_D8_report.tex';tex.write_text(pre+text)
    temp=ROOT/'tmp/pdfs/d8';temp.mkdir(parents=True,exist_ok=True)
    subprocess.run(['tectonic','--bundle',BUNDLE,'--keep-logs','--outdir',str(temp),str(tex)],cwd=ROOT,check=True)
    (ROOT/'output/pdf/manish_D8_report.pdf').write_bytes((temp/'manish_D8_report.pdf').read_bytes())
    subprocess.run(['pdftoppm','-scale-to','1300','-png',str(ROOT/'output/pdf/manish_D8_report.pdf'),str(temp/'page')],check=True)


if __name__=='__main__':main()
