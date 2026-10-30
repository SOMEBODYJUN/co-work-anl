#!/usr/bin/env python3
"""Read saved first-run witnesses; never rerun/import the original entrypoints.

Reconstruct every literal machine load from each saved assignment, and expose
why the coloring inflow uses target times rather than source times.  For the
8-machine instance, this checks the saved attaining assignments, not another
enumeration.  The original audit's 5184-state enumeration remains one run.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys


def read(path):
    return json.loads(path.read_text())


def main():
    base = Path(__file__).resolve().parent
    run = base / 'runs/original-replay-001'
    output = Path(sys.argv[1])
    assert not output.exists()
    counts = Counter()
    hashes = {}
    for p in sorted((run/'source').iterdir()):
        h = sha256(p.read_bytes()).hexdigest()
        assert h == sha256((base/'original'/p.name).read_bytes()).hexdigest()
        hashes[p.name] = h
    manifest = read(run/'input-manifest.json')
    for name, expected in manifest.items():
        assert sha256((run/'inputs'/name).read_bytes()).hexdigest() == expected
    commands = read(run/'commands.json')
    assert len(commands) == 2 and all(c['exit_code'] == 0 for c in commands)
    assert all((run/c['stderr']).read_bytes() == b'' for c in commands)

    def loads(P, machines, assignment):
        assert set(assignment) == set(P)
        L = dict.fromkeys(machines, F(0))
        for j, m in assignment.items():
            assert m in P[j] and m in L
            L[m] += F(P[j][m])
        counts['literal_complete_assignments'] += 1
        counts['literal_job_placements'] += len(P)
        counts['literal_machine_loads'] += len(machines)
        return L

    cases = read(run/'inputs/two_witness_query_separation_cases.json')['cases']
    saved = read(run/'query-audit.json')
    assert saved['script_sha256'] == hashes['two_witness_query_separation.py']
    assert saved['input_sha256'] == manifest['two_witness_query_separation_cases.json']
    differences = []
    for case, result in zip(cases, saved['cases']):
        assert case['id'] == result['case_id']
        P = {j['id']:j['processing'] for j in case['jobs']}
        M, T = case['machines'], F(case['T'])
        s0, s1, Q = case['sigma0'], case['sigma1'], case['queries']
        D = [j for j in P if s0[j] != s1[j]]
        colors = {a['job']:a['final_color'] for a in result['arcs']}
        target = {m:{q:sum((F(P[j][s1[j]]) for j in D if s1[j]==m and colors[j]==q),F(0)) for q in Q} for m in M}
        source = {m:{q:sum((F(P[j][s0[j]]) for j in D if s1[j]==m and colors[j]==q),F(0)) for q in Q} for m in M}
        assert target == {m:{q:F(v) for q,v in row.items()} for m,row in result['final_colored_inflow'].items()}
        for m in M:
            for q in Q:
                if target[m][q] != source[m][q]:
                    differences.append({'case':case['id'],'machine':m,'color':q,'correct_target_inflow':str(target[m][q]),'wrong_source_inflow':str(source[m][q])})
        reports = [result['sigma0'], result['sigma1'], *result['requested_tau']]
        reports += result.get('finite_enumeration',{}).get('states',[])
        for report in reports:
            L = loads(P,M,report['schedule'])
            assert L == {m:F(v) for m,v in report['loads'].items()}
            assert max(L.values(),default=F(0)) == F(report['peak'])
        for report in (result['sigma0'], result['sigma1']):
            assert F(report['peak']) <= T
        for tau in result['requested_tau']:
            q = tau['query']
            A = set(result['A_q'][q]); moved = {q}|A
            assert tau['schedule'] == {j:s1[j] if j in moved else s0[j] for j in P}
            delta = max((sum((F(P[r][s0[r]]) for r in Q if r!=q and s0[r]==m),F(0)) for m in M),default=F(0))
            assert F(tau['delta_q']) == delta
            assert F(tau['peak']) <= max(3*T/2,T+delta) == F(tau['theorem_bound'])
            fee = sum((F(case.get('nonquery_move_weights',{}).get(j,0)) for j in A),F(0))
            assert fee == F(tau['actual_nonquery_fee'])
        counts['query_complete_assignments'] += len(reports)
    assert counts['query_complete_assignments'] == 44 and differences

    take = read(run/'inputs/partial_sum_take_continue_flat_menu_actual_escape_independent_fraction_check_v1.json')
    menus = {}
    for a in range(1,4):
        menus[f'r_{a}'] = {'take1':{'u_1':'3/5',f'x_{a}':'2/5'}}
        menus[f'm_{a}'] = {'off':{f'x_{a}':'1'},'take2':{'u_2':'2/5',f'y_{a}':'3/5'}}
        menus[f'l_{a}'] = {'off':{f'y_{a}':'1'},'accept':{f'z_{a}':'1'}}
    P = {}; machines = set()
    for g, menu in menus.items():
        P['J:'+g] = {'M:'+g+':'+state:'1' for state in menu}
        for state, row in menu.items():
            private = 'M:'+g+':'+state; machines.add(private)
            for item,p in row.items():
                resource = 'R:'+item; machines.add(resource)
                P[f'I:{g}:{state}:{item}'] = {private:p,resource:'1'}
    assert menus == take['states'] and P == take['jobs']
    assert len(machines) == 26 and len(P) == 30 and sum(map(len,P.values())) == 57
    L = loads(P,machines,take['assignment'])
    assert L == {m:F(v) for m,v in take['loads'].items()} and max(L.values()) == F(8,5)
    seen = set(); qualities = {}
    for g, row in menus.items():
        selected = take['selected_states'][g]; B = take['bundles'][g]
        assert set(B) <= set(row[selected]) and not seen.intersection(B)
        seen.update(B)
        qualities[g] = sum((F(row[selected][u]) for u in B),F(0))
    assert qualities == {g:F(v) for g,v in take['qualities'].items()}
    assert min(qualities.values()) == F(2,5)

    root = read(run/'inputs/direct_cohabiting_sharp_unsat_root_integer_enumeration.json')
    other = read(run/'inputs/direct_cohabiting_sat_sharp_three_halves_independent_enum_v1.json')
    P = {}
    for i in range(4):
        P[f'q{i}'] = {f'M{i}':8,f'M{(i+1)%4}':10,f'C{i}':5}
        P[f'b{i}'] = {f'M{i if i<2 else (i+1)%4}':8,f'C{i}':10}
    P.update({'u+':{'C0':5,'C1':5},'u-':{'C2':5,'C3':5}})
    assert P == root['jobs'] and len(P) == 10 and sum(map(len,P.values())) == 24
    assert max(loads(P,root['machines'],root['one_optimal_assignment']).values()) == 15
    assert max(loads(other['jobs'],other['machines'],other['one_optimal_assignment']).values()) == 15
    assert loads(other['jobs'],other['machines'],other['baseline_assignment']) == {m:F(v) for m,v in other['baseline_loads'].items()}
    assert sum(root['peak_histogram_units'].values()) == 5184
    assert min(map(int,root['peak_histogram_units'])) == 15
    assert {int(k):v for k,v in root['peak_histogram_units'].items()} == {int(k):v for k,v in other['peak_histogram'].items()}
    fixed = read(run/'fixed-certificates-audit.json')
    assert fixed['take_continue']['optimization_run'] is False
    assert fixed['sharp_three_halves']['complete_assignments'] == 5184
    result = {'status':'passed','python':platform.python_version(),'scope':'saved-witness inspection, no source replay and no new assignment enumeration','counts':dict(counts),'target_vs_source_inflow_differences':differences,'source_sha256':hashes,'input_sha256':manifest,'new_original_entrypoint_runs':0,'new_complete_assignment_enumerations':0,'recovered_original_entrypoint_exit_codes':[c['exit_code'] for c in commands]}
    with output.open('x') as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'status':result['status'],'counts':result['counts'],'inflow_difference_count':len(differences),'new_original_runs':0,'new_enumerations':0}))


if __name__ == '__main__':
    main()
