"""Read the pinned source AST and one saved event; no original code is run."""
import argparse
import ast
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent

def fp(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--tax-source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    source=HERE/'original/deletion_36.py';raw=source.read_text();tree=ast.parse(raw);tax=args.tax_source.read_text();ast.parse(tax)
    assert fp(source)['sha256']=='b1c904461bf89c16ecee9d9e363aebd545d9a7117b5a7de4cf4ae2ff45ed0aef'
    assert fp(args.tax_source)['sha256']=='8f72ad4dc8464ef17883bce8f273faefe55152dd31b35aeee136c8bcf3579e21'
    loop=next(n for n in tree.body if isinstance(n,ast.For));assert ast.unparse(loop.iter)=='range(1)'
    n_assign=next(n for n in loop.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='n' for t in n.targets));assert ast.literal_eval(n_assign.value)==3
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='makepolicy' for n in ast.walk(tree))
    assert sum(isinstance(n,ast.Name) and n.id=='ww' and isinstance(n.ctx,ast.Load) for n in ast.walk(tree))==0
    assert not any(isinstance(n,ast.If) and '__name__' in ast.unparse(n.test) for n in tree.body)
    assert "replace('deletion_probe.py','deletion_candidate.json')" in raw
    assert 'deletion_36.py'.replace('deletion_probe.py','deletion_candidate.json')=='deletion_36.py'
    event=json.loads((HERE/'original-event/execution.json').read_bytes())
    stdout=(HERE/'original-event/stdout.txt').read_text();match=re.fullmatch(r'0 ([^ ]+) \(0, 3, 4\) ([^\n]+)\n',stdout);assert match
    assert event['exit_code']==0 and event['original_top_level_executions']==1
    assert event['deletion_probe_executions']==event['tax_probe_main_executions']==event['ExactSPESolver_calls']==0
    assert event['LP_invocations_if_normal_completion']==22 and event['entry_was_overwritten_by_original_output'] is False
    assert (HERE/'original-event/stderr.txt').read_bytes()==b'' and all(r['before']==r['after'] for r in event['input_files'])
    assert float(match.group(1))<0 and float(match.group(1))>-1e9
    queries=[{'index':a,'family':'pure','p':{str(a):'1'}} for a in range(6)]
    queries += [{'index':6+i,'family':'uniform_pair','p':{str(a):'1/2',str(b):'1/2'}} for i,(a,b) in enumerate(combinations(range(6),2))]
    queries += [{'index':21,'family':'uniform_all','p':{str(a):'1/6' for a in range(6)}}]
    report={'status':'PASS_STATIC_SOURCE_AND_EXECUTION_CONTRACT','inputs':[fp(source),fp(args.tax_source)],
      'actual_model':{'n':3,'k':6,'mask_interval':[1,63],'customer_variables':63,'auxiliary_t_variables':1,'normalized_customer_mass':'sum w=1','policy':'fixed opposite-group rule on all ordered histories','decision_histories':43,'IC_rows':258,'self_IC_rows':43,'nonself_IC_rows':215,'root':[0,3,4]},
      'LP_contract':{'query_distributions':queries,'LP_attempts_in_completed_entry':22,'variables':64,'inequality_rows_per_LP':261,'equality_rows_per_LP':1,'IC_t_column':'0','deletion_t_column':'1','objective':'W-(5/2)*t','t_bound':'0 <= t <= min_i E_p f_(z without i)','actual_deletion_backgrounds':[[3,4],[0,4],[0,3]],'all_query_distributions_searched':False,'all_legal_backgrounds_used':False,'exact_optimum_certificate_saved':False},
      'dependency_behavior':{'tax_prefix_inherited_n':4,'effective_n_after_override':3,'tax_prefix_initial_sigma_used_for_LP':False,'tax_main_calls':0,'tax_optimize_calls':0,'ww_random_seed':31289,'ww_used':False,'makepolicy_called':False,'ExactSPESolver_called':False,'original_import_triggers_optimization':True,'source_has_main_guard':False},
      'candidate_output':{'expression':"__file__.replace('deletion_probe.py','deletion_candidate.json')",'actual_basename_target':'deletion_36.py','self_overwrite_if_positive':True,'branch_taken_in_recorded_event':False,'candidate_saved':False,'rationalization_is_reverified':False,'minGamma_is_asserted':False,'t_saved':False,'target_recomputed_after_rationalization':False},
      'saved_event':{'stdout':stdout,'best_float_lexeme':match.group(1),'rounded_inner_seconds_lexeme':match.group(2),'process_wall_seconds':event['wall_seconds'],'exit_code':0,'stderr_bytes':0,'entry_unchanged':True,'all_six_inputs_unchanged':True,'best_query_and_weights_saved':False,'per_LP_statuses_saved':False},
      'mathematical_scope':'one fixed full SPE strategy cone, restricted actual-terminal deletion support and 22 predetermined p; not a full true-static-security optimization or a 36-customer input',
      'current_original_entries':0,'current_helper_calls':0,'current_LP_calls':0,'current_coefficient_reconstruction':0}
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'n':3,'queries':len(queries),'IC_rows':258,'original_calls':0,'LP_calls':0}))

if __name__=='__main__':main()
