"""Read saved reports and source AST; perform no LP, source import or IC scan.

This checks provenance and saved-data arithmetic. The independent source/model
coefficient and rational IC audit remains the separately executed shared record.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import Counter
import ast
import gzip
import hashlib
import json
import math
import sys

HERE=Path(__file__).resolve().parent
PROGRAM=HERE.parent/'fresh-global-two-probe-program'
CERTIFICATE=HERE.parent/'background-menu-certificate-data/original/background_menu_certificate.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    historical_path=HERE/'original/fresh_global_two_probe.json'
    historical=json.loads(historical_path.read_text())
    assert len(historical_path.read_bytes())==122
    assert sha(historical_path)=='ac507559105f4ffd6151124b859dcb20337694c48f69582540bc04d88f8160b7'
    assert list(historical)==['cases','policies','solved','best','seconds','found']
    assert historical==dict(cases=2000,policies=643,solved=13503,best=0.0,seconds=24.15056276321411,found=None)
    assert all(type(historical[k]) is int for k in ['cases','policies','solved'])
    assert type(historical['best']) is float and type(historical['seconds']) is float
    per_policy,rem=divmod(historical['solved'],historical['policies'])
    assert rem==0 and per_policy==21
    q=(math.isqrt(1+8*per_policy)-1)//2
    assert q==6 and q*(q+1)//2==per_policy

    source=PROGRAM/'original/probe_fresh_global_two.py'
    assert sha(source)=='6b5bf041c279d9d4def418444b266bdd8b4afdca46f336ea6cc28fa18857830c'
    tree=ast.parse(source.read_text(),filename=str(source))
    defaults={}
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='add_argument':
            for kw in n.keywords:
                if kw.arg=='default':defaults[ast.literal_eval(n.args[0])]=ast.literal_eval(kw.value)
    assert defaults=={'--q':6,'--cases':2000,'--seed':71213,'--max-background':4,'--output':'fresh_global_two_probe.json'}

    replay=PROGRAM/'replay'
    event_path=replay/'execution.json';event=json.loads(event_path.read_text())
    new_path=replay/'runtime/bounded_probe.json';new=json.loads(new_path.read_text())
    compressed_path=replay/'lp-capture.json.gz'
    captured_bytes=gzip.decompress(compressed_path.read_bytes())
    capture=json.loads(captured_bytes)
    exact_path=PROGRAM/'contract-audit.json';exact=json.loads(exact_path.read_text())
    assert hashlib.sha256(captured_bytes).hexdigest()==exact['capture_sha256']=='f8a4572d3d669f7eb9c2200ceb5bf21d90fd4dd1c5afd10a3ba6fabe35cc6e37'
    assert len(captured_bytes)==3108955
    assert event['argv'][1:]==['--q','6','--cases','4','--seed','71213','--max-background','4','--output','bounded_probe.json']
    assert event['original_main_calls']==1 and event['lp_calls']==84 and event['exit_code']==0 and event['exception'] is None
    assert event['source_sha256_before']==event['source_sha256_after']==sha(source)
    assert {k:v for k,v in new.items() if k!='seconds'}==dict(cases=4,policies=4,solved=84,best=0.0,found=None)
    assert new['seconds']>0 and (replay/'stderr.txt').read_bytes()==b''
    assert json.loads((replay/'stdout.txt').read_text().splitlines()[-1])==new
    assert exact['status']=='PASS'
    assert all(exact[k]==0 for k in ['original_imports','original_helpers','original_main','lp_calls'])
    assert exact['successful_observed_lp_calls']==exact['exact_feasible_reconstructions']==84
    assert exact['unique_matrix_coefficients']==8820
    assert exact['objective_coefficients']==exact['certificate_link_identities']==5292
    assert exact['exact_ic_evaluations']==2940

    pairs=list(combinations_with_replacement(range(6),2))
    assert len(capture)==len(exact['records'])==84 and len(exact['policies'])==4
    status=Counter();float_sign=Counter();rational_values=Counter();policies=[]
    saved_slack_entries=saved_weight_entries=0
    for case in range(4):
        block=capture[case*21:(case+1)*21]
        policy=exact['policies'][case];first=block[0]
        expected_labels=[['last',a,b] for a in range(6) for b in range(6) if b!=policy['reply'][a]]
        expected_labels += [['root',a] for a in range(6) if a!=policy['actual']]
        assert policy['case']==case and policy['L']==case+1 and policy['row_labels']==expected_labels
        assert len(first['A_ub'])==35 and all(len(row)==63 for row in first['A_ub'])
        assert all(math.isfinite(x) for row in first['A_ub'] for x in row)
        policies.append({k:v for k,v in policy.items() if k!='row_labels'})
        for j,(record,pair) in enumerate(zip(block,pairs,strict=True)):
            assert record['case']==case and record['L']==case+1
            assert record['actual']==policy['actual'] and record['response']==policy['reply']
            assert record['compare']==list(pair) and record['A_ub']==first['A_ub']
            assert record['b_ub']==[0.]*35 and record['A_eq']==[[1.]*63] and record['b_eq']==[1]
            assert record['bounds']==[0,None] and record['method']=='highs'
            assert len(record['c'])==63 and all(math.isfinite(x) for x in record['c'])
            result=record['result'];status[str(result['status'])]+=1
            assert result['success'] and result['status']==0 and len(result['x'])==63
            assert all(math.isfinite(x) for x in result['x']) and math.isfinite(result['fun'])
            fun=result['fun'];float_sign['negative' if fun<0 else 'positive' if fun>0 else 'zero']+=1
            saved=exact['records'][case*21+j]
            assert (saved['case'],saved['L'],saved['compare'])==(case,case+1,list(pair))
            assert saved['floating_fun']==fun
            value=F(saved['exact_feasible_value']);rational_values[str(value)]+=1
            slacks=[F(x) for x in saved['exact_ic_slacks']]
            assert len(slacks)==35 and min(slacks)>=0
            saved_slack_entries+=len(slacks)
            weights={int(k):F(v) for k,v in saved['nonzero_weights'].items()}
            assert weights and all(1<=k<=63 and v>0 for k,v in weights.items()) and sum(weights.values())==1
            saved_weight_entries+=len(weights)
            multipliers={int(k):F(v) for k,v in saved['certificate_multipliers'].items()}
            assert all(0<=k<35 and v>0 for k,v in multipliers.items())
            contribution=sum(v*slacks[k] for k,v in multipliers.items())
            remainder=F(saved['nonnegative_remainder'])
            assert contribution==F(saved['ic_contribution']) and remainder>=0 and value==contribution+remainder
            assert abs(fun-float(value))<=1e-15
    assert dict(rational_values)==exact['exact_values'] and rational_values['0']==10
    assert float_sign==Counter(negative=2,zero=8,positive=74)
    assert min(r['result']['fun'] for r in capture)==exact['floating_min']
    assert max(r['result']['fun'] for r in capture)==exact['floating_max']
    certificate=json.loads(CERTIFICATE.read_text())
    assert certificate=={'success':True,'labels':'ABTSQRHV','slacks':{'floor_B':'1/2','floor_H':'1','last_B_A_T':'1','last_B_A_S':'1'},'cases':384,'minimum':'0'}
    bindings=[historical_path,source,event_path,new_path,compressed_path,exact_path,CERTIFICATE]
    out={'status':'PASS','kind':'saved-record provenance and arithmetic audit; no model or optimization rerun',
         'new_original_entries':0,'new_lp_calls':0,'new_independent_coefficient_or_ic_evaluations':0,
         'historical_fields':historical,'source_defaults_not_historical_metadata':defaults,
         'conditional_inference':{'assumption':'this generator produced this report and reached its normal complete return','comparison_pairs_per_policy':21,'q':6,'multiplication':'643 * 21 = 13503','configured_cases':2000},
         'historical_unknowns':['exact argv','seed','max_background','background lengths represented','environment','all 643 policy keys','per-LP success/status/values','exact optimality','exact customer or strategy witness'],
         'shared_current_event':{'policies':policies,'original_entries':1,'lp_calls':84,'status_counts':dict(status),'float_sign_counts':dict(float_sign),'floating_min':exact['floating_min'],'floating_max':exact['floating_max'],'inner_report_seconds':new['seconds'],'outer_event_seconds':event['elapsed_seconds'],'independent_feasible_reconstructions':84,'exact_value_counts':dict(rational_values),'exact_zero_problems':10,'positive_feasible_values_without_exact_optimality_certificate':74},
         'saved_structure_checked':{'capture_bytes_decompressed':len(captured_bytes),'capture_records':84,'distinct_policy_matrices':4,'matrix_dimensions':[35,63],'each_policy_all_comparison_pairs':21,'saved_nonnegative_ic_slacks_read':saved_slack_entries,'saved_positive_rational_weight_entries_read':saved_weight_entries,'objective_decomposition_records':84},
         'analytical_scope':'Existing four-multiplier legal H certificate proves the restricted domain; general-background GLOBAL is false. No old 384-row or 52-client audit repeated.',
         'bindings':[{'path':str(p.relative_to(HERE.parents[4])),'bytes':p.stat().st_size,'sha256':sha(p)} for p in bindings]}
    output=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'report-audit.json'
    output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','historical_fields':6,'shared_records':84,'shared_policies':4,'saved_IC_slacks_read':saved_slack_entries,'new_math_entries':0,'output':str(output)}))

if __name__=='__main__':main()
