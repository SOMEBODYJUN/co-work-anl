"""Static reading of the six-field historical report and pinned generator AST.

No original function, arithmetic block, optimizer, or random generator is run.
The legal-H theorem and one synthetic arithmetic audit are reused separately.
"""
import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path

def fp(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--report',type=Path,default=Path(__file__).parent/'original/fresh_arbitrary_probe.json')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();assert __debug__
    raw=args.source.read_text();tree=ast.parse(raw)
    report=json.loads(args.report.read_bytes())
    assert fp(args.source)['sha256']=='efdfe17ac4a1751fc784c2c833e59d6fb5443935d6fce4c19aca148a5f191a12'
    assert fp(args.report)['sha256']=='e444f6a49b0e20becece58c11b96437fb5f190e008d3f4d2b67aacd90d7bd02a'
    assert report=={'q':7,'cases':12000,'background_repetitions':1,'feasible':12000,'best':0.0,'seconds':32.25970125198364}
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
    best_writes=[n for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store) and n.id=='best']
    assert len(best_writes)==1
    best_assignment=next(n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='best' for t in n.targets))
    assert ast.literal_eval(best_assignment.value)==0.0
    best_comparison=next(n for n in ast.walk(fn) if isinstance(n,ast.Compare) and any(isinstance(c,ast.Name) and c.id=='best' for c in ast.walk(n)))
    assert ast.unparse(best_comparison)=='res.fun < best - 1e-08'
    terminal=fn.body[-1];assert isinstance(terminal,ast.Return) and isinstance(terminal.value,ast.Call)
    assert terminal.value.func.id=='dict'
    terminal_fields={k.arg:ast.unparse(k.value) for k in terminal.value.keywords}
    assert list(terminal_fields)==list(report) and 'seed' not in terminal_fields
    defaults={}
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='add_argument':
            defaults[ast.literal_eval(n.args[0])]=next(ast.literal_eval(k.value) for k in n.keywords if k.arg=='default')
    assert defaults=={'--q':6,'--cases':10000,'--seed':71215,'--background':1}
    meanings={
      'q':'seven action labels 0..6, not customers or providers',
      'cases':'12000 draws with replacement; distinct maps and historical seed not recorded',
      'background_repetitions':'one occurrence of the legal topic H=0; p=I_H, not arbitrary background loads',
      'feasible':'count of res.success; no saved optimizer vectors or exact SPE witnesses',
      'best':'constant zero initialized once and never updated; terminal negative-threshold sentinel, not a minimum',
      'seconds':'historical time.time difference around the loop, after utility construction, before final JSON write'}
    q,L=report['q'],report['background_repetitions']
    out={'status':'PASS_STATIC_REPORT_AND_SOURCE_CONTRACT',
      'inputs':[fp(args.report),fp(args.source)],'original_fields':report,
      'all_six_field_interpretations':[{'field':k,'saved_value':v,'meaning':meanings[k]} for k,v in report.items()],
      'source_AST':{'run_arguments':[a.arg for a in fn.args.args],'terminal_return_fields':terminal_fields,
        'best_store_count':len(best_writes),'best_initial_value':0.0,'early_return_test':ast.unparse(best_comparison),
        'CLI_defaults':defaults,'historical_seed_in_report':False,'defaults_are_historical_seed_evidence':False},
      'decoded_report_domain':{'q':q,'L':L,'mask_interval_inclusive':[1,2**q-1],'mask_bit_definition':'I_a(m)=(m>>a)&1','customer_types':2**q-1,
        'H':0,'actual_A':1,'actual_B':2,'compare_T':3,'compare_S':4,'role_labels_are_distinct':True,'coverages_need_not_be_distinct':True,
        'variables':'nonnegative real normalized customer masses, sum w=1','last_IC_rows':q*(q-1),'first_IC_rows':q-1,'total_IC_rows':q*q-1,
        'utility_entries_per_map':q*q*(2**q-1),'IC_coefficients_per_map':(q*q-1)*(2**q-1),'objective_coefficients':2**q-1,
        'reply_maps_with_fixed_rA_B':q**(q-1),'draws_with_replacement':report['cases'],'distinct_sample_count':None,'historical_seed':None,
        'objective':'U(A,B)+U(B,A)+fresh_coverage(A union B)-fresh_coverage(T union S)'},
      'analytic_common_feasible_point':{'mask':2**q-1,'mass':'1','all_other_masses':'0','all_IC_values':'0','per_player_profit':f'1/{L+2}','objective':f'2/{L+2}',
        'reason':'all topics cover the same old customer, so all action and continuation payoffs coincide; independent of sampled reply map'},
      'interpretation_limits':['no historical graph list or per-LP objective values','best is not an optimum','no full-root reachability certificate','single legal background topic only','fixed distinct role labels, not every coincidence pattern','no current rerun of historical LP search'],
      'current_original_function_calls':0,'current_original_main_calls':0,'current_original_AST_arithmetic_executions':0,'current_LP_calls':0,'current_random_draws':0,
      'shared_synthetic_audit':'one q7/L1/seed0 graph, owned by companion program; not run by this inspector',
      'legal_H_nonnegativity':'reused exact four-multiplier certificate and nonnegative safety differences, not inferred from historical finite sampling'}
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'fields':len(report),'customer_types':2**q-1,'IC_rows':q*q-1,'possible_maps':q**(q-1),'original_calls':0,'LP_calls':0}))

if __name__=='__main__':main()
