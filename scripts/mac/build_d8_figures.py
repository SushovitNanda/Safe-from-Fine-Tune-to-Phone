"""Article figures from text-free D7 summaries and independently reproduced ratios."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'reports/D8/figures';OUT.mkdir(parents=True,exist_ok=True)
old=json.loads((ROOT/'handoff/D7_2026-11-08/summary.json').read_text())['cells'];new=json.loads((ROOT/'handoff/D7_2026-11-10/summary.json').read_text())['cells']
analysis=json.loads((ROOT/'results/mac/nov11/analysis/deployment_analysis.json').read_text())
settings=['f16','q4km','q3km','q4km-nopre','budget-phone'];names=['F16','Q4','Q3','Q4 no preamble','Phone stack'];colors=['#087f8c','#c75b37']
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})

def save(fig,name):
    fig.savefig(OUT/f'{name}.png',bbox_inches='tight');fig.savefig(OUT/f'{name}.pdf',bbox_inches='tight');plt.close(fig)

fig,axes=plt.subplots(2,2,figsize=(10,6.6),sharey=True,layout='constrained')
for ax,lang in zip(axes.flat,['all','en','hi','hinglish']):
    x=np.arange(5)
    for prefix,source,color,offset,label in [('med',old,colors[1],-.07,'Medical'),('rep_steer',new,colors[0],.07,'Medical + steering')]:
        data=[source[f'mac__{prefix}_{s}'][f'asr|pooled|{lang}'] for s in settings];y=np.array([r['rate'] for r in data]);lo=np.array([r['ci95'][0] for r in data]);hi=np.array([r['ci95'][1] for r in data])
        ax.errorbar(x+offset,y,yerr=[y-lo,hi-y],fmt='o-',capsize=3,color=color,label=label,lw=1.3)
    ax.set_title({'all':'Pooled','en':'English','hi':'Hindi','hinglish':'Hinglish'}[lang]);ax.set_xticks(x,names,rotation=18,ha='right');ax.set_ylim(0,85);ax.grid(axis='y',alpha=.2)
    if lang in ['all','hi']:ax.set_ylabel('Harmful-prompt ASR (%)')
axes[0,0].legend(frameon=False,fontsize=9);fig.suptitle('Steering lowers ASR, with large residual language differences',fontsize=13)
save(fig,'rq5_asr_languages')

fig,ax=plt.subplots(figsize=(9,4.4),layout='constrained')
for j,(lang,color) in enumerate(zip(['all','en','hi','hinglish'],['#183548','#087f8c','#c75b37','#8064a2'])):
    rs=[analysis['retention'][f'{s}|pooled|{lang}'] for s in settings[1:]];y=np.array([r['retention'] for r in rs]);lo=np.array([r['ci95'][0] for r in rs]);hi=np.array([r['ci95'][1] for r in rs]);x=np.arange(4)+(j-1.5)*.12
    ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt='o',capsize=3,color=color,label={'all':'Pooled','en':'English','hi':'Hindi','hinglish':'Hinglish'}[lang])
ax.axhline(1,color='black',ls='--',lw=1);ax.set_xticks(np.arange(4),names[1:]);ax.set_ylabel('Repair retention R(s)');ax.set_ylim(0,2.5);ax.set_title('All pooled retention intervals include 1');ax.legend(ncol=4,frameon=False,loc='upper center');ax.grid(axis='y',alpha=.2)
save(fig,'rq5_retention')

fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True,layout='constrained')
for ax,kind in zip(axes,['benign_general','benign_clinical']):
    x=np.arange(5)
    for prefix,source,color,offset,label in [('med',old,colors[1],-.17,'Medical'),('rep_steer',new,colors[0],.17,'Medical + steering')]:
        data=[source[f'mac__{prefix}_{s}'][f'over_refusal|{kind}|all'] for s in settings];y=np.array([r['rate'] for r in data]);ax.bar(x+offset,y,.32,color=color,label=label)
    ax.set_xticks(x,names,rotation=20,ha='right');ax.set_title(kind.replace('benign_','').title());ax.grid(axis='y',alpha=.2)
axes[0].set_ylabel('Pooled benign-prompt ORR (%)');axes[0].legend(frameon=False,fontsize=9);fig.suptitle('Safety gains carry an over-refusal cost; pooled ORR includes directional Hinglish',fontsize=11)
save(fig,'rq5_overrefusal')

roi=json.loads((ROOT/'results/mac/nov11/roi_evidence.json').read_text());r=roi['base_result'];s=roi['base_scenario'];volume=np.linspace(0,100000,300);api_each=(s['input_tokens_per_request']*s['api_input_per_million']+s['output_tokens_per_request']*s['api_output_per_million'])/1e6
fig,ax=plt.subplots(figsize=(8.5,4.2),layout='constrained');ax.plot(volume/1000,volume*api_each,label='API listed-price token-budget scenario',color=colors[1]);ax.plot([0,r['capacity_requests_per_month']/1000],[r['monthly_local_cost']]*2,label='Assumed fixed local monthly budget',color=colors[0]);ax.axvspan(r['capacity_requests_per_month']/1000,100,color='#999',alpha=.13,label='Beyond assumed local capacity');ax.axvline(r['capacity_requests_per_month']/1000,color='#555',ls=':',label='Evaluation-based capacity proxy');ax.axvline(r['break_even_requests_per_month']/1000,color='#888',ls='--',label='Conditional break-even');ax.set_xlabel('Hypothetical requests per month (thousands)');ax.set_ylabel('USD per month');ax.set_title('Illustrative costs; clinic demand, power and quality equivalence unmeasured');ax.legend(frameon=False,fontsize=8);ax.grid(alpha=.2)
save(fig,'roi_conditional_scenario')
print('Wrote four standalone PNG/PDF figures to',OUT)

# RQ6: show pooled rates and direct contrasts; audited Hinglish scores are not a safety effect.
rq6=json.loads((ROOT/'handoff/D7_2026-11-11/laptop_rq6_analysis.json').read_text())['rq6']
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
tags=['stock','protected','random'];x=np.arange(3)
for metric,ax in zip(['asr','clinical_orr'],axes):
    values=[rq6['rates'][t]['all'] if metric=='asr' else rq6['orr']['clinical|all'][t] for t in tags]
    y=np.array([r['rate'] for r in values]);lo=np.array([r['ci95'][0] for r in values]);hi=np.array([r['ci95'][1] for r in values])
    ax.bar(x,y,color=['#183548','#087f8c','#c75b37'],width=.62)
    ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt='none',ecolor='#333',capsize=4)
    for xx,yy in zip(x,y):ax.text(xx,yy+6,f'{yy:.1f}%',ha='center')
    ax.set_xticks(x,['Stock','Protected','Random']);ax.set_ylim(0,60);ax.grid(axis='y',alpha=.2)
    ax.set_ylabel('Pooled ASR (%)' if metric=='asr' else 'Pooled clinical ORR (%)')
    ax.set_title('No pooled protection benefit' if metric=='asr' else 'Higher clinical over-refusal')
fig.suptitle('RQ6: identical steering, corrected matched-size Q3 builds',fontsize=13)
fig.supxlabel('Frozen primary judges; Hinglish safety artefact and directional ORR limit pooled interpretation',fontsize=9)
save(fig,'rq6_protection')
print('Wrote final RQ6 figure; five figure pairs total')
