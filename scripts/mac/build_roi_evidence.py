"""M21 measured evaluation-throughput plus explicitly conditional cost scenarios."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from roi import calculate


def main():
    rows={}
    for cell in ['rep_steer_f16','rep_steer_q4km','rep_steer_q3km','rep_steer_q4km-nopre','rep_steer_budget-phone']:
        p=ROOT/f'models/local-results/day7/{cell}.jsonl';records=[json.loads(x) for x in p.read_text().splitlines()];summary=json.loads(p.with_suffix('.summary.json').read_text())
        if len(records)!=1612 or not summary['complete'] or summary['errors'] or summary['new_responses']!=1612:raise ValueError('ROI benchmark requires complete single-session stopped full cells')
        if any(r['stop_token_ids']!=[3,6] for r in records):raise ValueError('Incomparable stopping policy')
        rows[cell]={'requests':1612,'wall_seconds':summary['session_seconds'],'requests_per_second':1612/summary['session_seconds'],'completion_tokens_per_second':summary['session_tokens_per_second'],'mean_prompt_tokens':sum(r['token_usage']['prompt_tokens'] for r in records)/1612,'mean_completion_tokens':sum(r['token_usage']['completion_tokens'] for r in records)/1612,'capped_256':sum(r['token_usage']['completion_tokens']==256 for r in records),'workload':'Fixed safety/benign evaluation; eight concurrent slots, includes input prefill; not validated clinic/useful-answer throughput'}
    price={'model':'gpt-4.1-mini','status_at_source':'deprecated reference, not a deployment recommendation','input_USD_per_million':.40,'output_USD_per_million':1.60,'cached_input_used':False,'source':'https://developers.openai.com/api/docs/models/gpt-4.1-mini','verified_date_IST':'2026-11-11','token_budget_note':'Numerically equal token budgets only; API tokenizer/billed usage and quality equivalence were not measured.'}
    q=rows['rep_steer_q3km']
    scenario={'illustrative_only':True,'currency':'USD','assumptions_source':'Measured Mac steeredQ3 evaluation throughput and token means; official listed GPT4.1mini price verified2026-11-11 (deprecated reference); all demand, hardware valuation, allocation, hours, power, electricity and support costs below are assumed sensitivity inputs. Not clinic savings or capability-equivalent model pricing.','requests_per_month':10000,'input_tokens_per_request':q['mean_prompt_tokens'],'output_tokens_per_request':q['mean_completion_tokens'],'api_input_per_million':.40,'api_output_per_million':1.60,'hardware_cost':600,'amortization_months':36,'hardware_allocation':.5,'available_hours_per_month':30,'utilization':.5,'requests_per_second':q['requests_per_second'],'wall_power_watts':40,'electricity_per_kwh':.2,'other_local_monthly_cost':5}
    evidence={'stopped_evaluation_benchmarks':rows,'price_reference':price,'base_scenario':scenario,'base_result':calculate(scenario),'sensitivity':[],'clinical_ROI_established':False,'limitations':['No measured wall power, clinic traffic, peak queueing or clinical latency target','Degenerate/repetitive text remains present; generated tokens are not useful clinical work','API tokenization, quality, safety and output billing are not equivalent measurements','No retrofit use of old EOS3-only capped timings; all benchmarks here stop3,6','Hardware, electricity, operating budget and demand are assumptions; no spending recommendation']}
    for n in [1000,10000,50000]:
        for w in [20,40,60]:
            s={**scenario,'requests_per_month':n,'wall_power_watts':w};evidence['sensitivity'].append({'requests':n,'assumed_power_W':w,**calculate(s)})
    (ROOT/'configs/mac/nov11/roi_evaluation_scenario.json').write_text(json.dumps(scenario,indent=2)+'\n')
    (ROOT/'results/mac/nov11/roi_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('Measured benchmark RPS:',q['requests_per_second'],'conditional costs:',evidence['base_result']['monthly_local_cost'],evidence['base_result']['monthly_api_cost'])


if __name__=='__main__':main()
