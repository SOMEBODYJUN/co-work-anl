#!/usr/bin/env python3
"""Replay the two new original entrypoints and check literal result schedules.

No original module is imported. The trace checker recomputes target-time
inflows from the original P, rather than trusting incremental/boolean fields.
The fixed-matrix auditor itself performs the single 5184-state enumeration;
this wrapper does not repeat that enumeration or claim a generic solver.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def query_recheck(raw, output):
    counts=Counter(); summaries=[]
    assert output['case_count']==len(raw['cases'])==3 and output['all_checks_passed']
    assert output['claim_reference']==raw['claim']
    for case,result in zip(raw['cases'],output['cases']):
        machines=case['machines'];jobs=[j['id'] for j in case['jobs']]
        P={j['id']:{m:F(t) for m,t in j['processing'].items()} for j in case['jobs']}
        sigma0,sigma1=case['sigma0'],case['sigma1'];T=F(case['T']);Q=case['queries']
        D=[j for j in jobs if sigma0[j]!=sigma1[j]];N=[j for j in D if j not in Q]
        weights={j:F(case.get('nonquery_move_weights',{}).get(j,0)) for j in N}
        fixed={m:sum((P[j][sigma0[j]] for j in jobs if j not in D and sigma0[j]==m),F(0)) for m in machines}
        assert result['case_id']==case['id'] and result['D']==D and result['Q']==Q and F(result['T'])==T
        assert result['original_machine_count']==len(machines) and result['original_job_count']==len(jobs)
        counts['original_input_finite_edges']+=sum(map(len,P.values()))

        def schedule(report):
            sigma=report['schedule'];assert set(sigma)==set(jobs)
            loads=dict.fromkeys(machines,F(0));by_machine={m:[] for m in machines}
            for j in jobs:
                m=sigma[j];assert m in P[j];loads[m]+=P[j][m]
                by_machine[m].append({'job':j,'processing_time':str(P[j][m])})
            assert loads=={m:F(v) for m,v in report['loads'].items()}
            assert by_machine==report['jobs_by_machine']
            peak=max(loads.values(),default=F(0));assert peak==F(report['peak'])
            assert report['peak_machines']==[m for m in machines if loads[m]==peak]
            counts['complete_schedule_records']+=1;counts['actual_job_assignments']+=len(jobs);counts['all_machine_loads']+=len(machines)
            return sigma,peak
        for key,expected in (('sigma0',sigma0),('sigma1',sigma1)):
            sigma,peak=schedule(result[key]);assert sigma==expected and peak<=T
        color={j:j if j in Q else None for j in D};machine_color=dict.fromkeys(machines)
        def inflows():
            return {m:{q:sum((P[j][sigma1[j]] for j in D if color[j]==q and sigma1[j]==m),F(0)) for q in Q} for m in machines}
        for step,event in enumerate(result['trigger_trace'],1):
            inflow=inflows();candidates=[(m,q) for m in machines if machine_color[m] is None for q in Q if inflow[m][q]>T/2]
            assert candidates and candidates[0]==(event['machine'],event['color'])
            m,q=candidates[0];assert event['step']==step and F(event['inflow_at_trigger'])==inflow[m][q] and F(event['strict_threshold'])==T/2
            machine_color[m]=q
            outgoing=[j for j in N if sigma0[j]==m]
            assert [z['job'] for z in event['newly_colored_arcs']]==outgoing
            for j,update in zip(outgoing,event['newly_colored_arcs']):
                assert color[j] is None;color[j]=q;target=sigma1[j]
                assert update['target']==target and F(update['added_inflow'])==P[j][target]
                assert F(update['new_color_inflow_at_target'])==inflows()[target][q]
            counts['valid_strict_machine_triggers']+=1
        final=inflows();assert not [(m,q) for m in machines if machine_color[m] is None for q in Q if final[m][q]>T/2]
        assert machine_color==result['machine_colors']
        assert fixed=={m:F(v) for m,v in result['stationary_loads'].items()}
        assert final=={m:{q:F(v) for q,v in row.items()} for m,row in result['final_colored_inflow'].items()}
        assert F(result['trigger_threshold'])==T/2
        for m in machines:
            assert fixed[m]+sum(final[m].values(),F(0))<=T
            for q in Q:
                assert (final[m][q]>T/2) if machine_color[m]==q else (final[m][q]<=T/2)
        assert result['arcs']==[{'job':j,'source':sigma0[j],'target':sigma1[j],'source_time':str(P[j][sigma0[j]]),'target_time':str(P[j][sigma1[j]]),'final_color':color[j]} for j in D]
        A={q:[j for j in jobs if j in N and color[j]==q] for q in Q}
        assert A==result['A_q'] and result['uncolored_nonquery']==[j for j in N if color[j] is None]
        assert sum(len(v) for v in A.values())==len(set(j for row in A.values() for j in row))
        fees={q:sum((weights[j] for j in A[q]),F(0)) for q in Q};W=sum(weights.values(),F(0))
        assert fees=={q:F(v) for q,v in result['c_q'].items()} and F(result['W'])==W and F(result['sum_c_q'])==sum(fees.values(),F(0))<=W
        tau_values=[]
        for tau in result['requested_tau']:
            q=tau['query'];sigma,peak=schedule(tau);changed={q,*A[q]}
            assert sigma=={j:sigma1[j] if j in changed else sigma0[j] for j in jobs}
            assert tau['changed_jobs']==[j for j in jobs if j in changed] and tau['A_q']==A[q]
            delta=max((sum((P[r][sigma0[r]] for r in Q if r!=q and sigma0[r]==m),F(0)) for m in machines),default=F(0))
            bound=max(3*T/2,T+delta)
            assert F(tau['delta_q'])==delta and F(tau['theorem_bound'])==bound and peak<=bound
            assert F(tau['actual_nonquery_fee'])==F(tau['support_fee'])==fees[q]
            tau_values.append({'q':q,'peak':str(peak),'delta':str(delta),'bound':str(bound),'fee':str(fees[q])})
        if 'finite_enumeration' in result:
            enumeration=result['finite_enumeration'];states=enumeration['states'];seen=set()
            assert enumeration['D_bit_order']==D and enumeration['state_count']==len(states)==2**len(D)==32
            assert enumeration['all_finite_endpoint_assignments_covered']==all(set(P[j])=={sigma0[j],sigma1[j]} for j in jobs)
            for state in states:
                sigma,peak=schedule(state);bits=tuple(state['state_bits_in_D_order']);assert bits not in seen;seen.add(bits)
                assert len(bits)==len(D) and set(bits)<={0,1}
                moved={j for j,bit in zip(D,bits) if bit}
                assert sigma=={j:sigma1[j] if j in moved else sigma0[j] for j in jobs}
                assert state['query_subset']==[q for q in Q if q in moved] and state['changed_nonquery']==[j for j in N if j in moved]
                assert F(state['nonquery_move_fee'])==sum((weights[j] for j in N if j in moved),F(0))
            for check in enumeration['threshold_checks']:
                feasible=[s for s in states if set(s['query_subset'])==set(check['query_subset']) and F(s['peak'])<=F(check['cap'])]
                assert len(feasible)==check['feasible_state_count']
                assert min(F(s['nonquery_move_fee']) for s in feasible)==F(check['minimum_fee'])
                mandatory=set.intersection(*(set(s['changed_nonquery']) for s in feasible))
                assert check['mandatory_changed_nonquery']==[j for j in N if j in mandatory]
            for check in enumeration['minimum_peak_checks']:
                feasible=[s for s in states if set(s['query_subset'])==set(check['query_subset']) and F(s['nonquery_move_fee'])<=F(check['fee_at_most'])]
                assert min(F(s['peak']) for s in feasible)==F(check['minimum_peak'])
            counts['finite_two_endpoint_states_rechecked']+=len(states)
        summaries.append({'case_id':case['id'],'A_q':A,'W':str(W),'sum_fees':str(sum(fees.values(),F(0))),'tau':tau_values})
    return dict(counts),summaries


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-dir',required=True);args=parser.parse_args()
    base,run=Path(__file__).resolve().parent,Path(args.run_dir).resolve();run.mkdir(parents=True,exist_ok=False)
    source,inputs=run/'source',run/'inputs';source.mkdir();inputs.mkdir()
    for p in (base/'original').iterdir():
        if p.is_file():shutil.copy2(p,(source if p.suffix=='.py' else inputs)/p.name)
    names=['partial_sum_take_continue_flat_menu_actual_escape_independent_fraction_check_v1.json','direct_cohabiting_sharp_unsat_root_integer_enumeration.json','direct_cohabiting_sat_sharp_three_halves_independent_enum_v1.json']
    for name in names:shutil.copy2(base/'comparisons'/name,inputs/name)
    commands=[]
    def command(name,script,arguments):
        argv=[sys.executable,str(source/script),*map(str,arguments)];p=subprocess.run(argv,capture_output=True,text=True)
        (run/(name+'.stdout')).write_text(p.stdout);(run/(name+'.stderr')).write_text(p.stderr)
        commands.append({'name':name,'argv':argv,'cwd':str(Path.cwd()),'exit_code':p.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'})
        dump(run/'commands.json',commands);assert p.returncode==0,name
    case_path=inputs/'two_witness_query_separation_cases.json'
    command('query-audit','two_witness_query_separation.py',['--input',case_path,'--output',run/'query-audit.json'])
    command('fixed-certificates-audit','audit_query_return_source_fixed_certificates.py',['--take-certificate',inputs/names[0],'--sharp-certificate',inputs/names[1],'--independent-sharp-certificate',inputs/names[2],'--output',run/'fixed-certificates-audit.json'])
    query=json.loads((run/'query-audit.json').read_text());raw=json.loads(case_path.read_text())
    counts,summaries=query_recheck(raw,query)
    fixed=json.loads((run/'fixed-certificates-audit.json').read_text())
    assert fixed['take_continue']['optimization_run'] is False
    assert fixed['sharp_three_halves']['complete_assignments']==5184 and fixed['sharp_three_halves']['exact_opt']=='3/2'
    input_hashes={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(inputs.iterdir())}
    dump(run/'input-manifest.json',input_hashes)
    report={'status':'passed','python':platform.python_version(),'query_literal_counts':counts,'query_cases':summaries,'fixed_matrix_audit':fixed,'commands':commands,
            'source_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(source.iterdir())},'input_sha256':input_hashes,
            'scope':'Two original entrypoints each run once. Query checker independently rechecked all 44 saved complete schedules/trace invariants; only the listed 32 endpoint states were rechecked. Original fixed auditor enumerated exactly 5184 assignments for one 8-machine matrix; take/continue only checked a complete attaining witness, not optimization. No general scheduler, source reduction, v3 selector or global price backend.'}
    dump(run/'verification.json',report)
    print(json.dumps({'status':'passed','query_counts':counts,'fixed_sharp_assignments':5184,'take_optimization_run':False},ensure_ascii=False))


if __name__=='__main__':main()
