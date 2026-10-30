#!/usr/bin/env python3
"""New half-density/profile entrypoints, independent literal/forest recheck.

Original sources are copied byte-for-byte to external snapshots. The 5001-digit
half-density CLI boundary is run once with the standard 4300 digit limit and
once with that limit explicitly disabled; neither source is edited.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def dump(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def recheck(data, result):
    k, h = int(data['k']), int(data['h'])
    capacities = list(map(int, data['clause_capacities']))
    nodes, roots, trees, degree = {}, [], [], Counter()
    for v, variable in enumerate(data['variables']):
        pair = []
        for sign, name in enumerate(('positive', 'negative')):
            leaves = {tuple(z['path']): z['clause'] for z in variable[name]}
            assert len(leaves) == len(variable[name]) == k ** h
            parents = sorted({p[:d] for p in leaves for d in range(h)}, key=lambda p: (len(p), p))
            for p in parents: nodes[v, sign, p] = len(nodes)
            pair.append(nodes[v, sign, ()]); trees.append((v, sign, leaves, parents))
            degree.update(leaves.values())
        roots.append(pair)
    internal = len(nodes); bases = []; cursor = internal
    ranges = []
    for c, a in enumerate(capacities):
        bases.append(cursor)
        ranges.append({'clause': c, 'start': cursor, 'count': a, 'arity': degree[c], 'listed_units': min(a, degree[c]), 'matching_units': (degree[c]+1)//2})
        assert degree[c] <= 2*a
        cursor += a
    jobs, outgoing, incoming = [], {u: [] for u in range(internal)}, {}
    ports = [[] for _ in capacities]
    for v, pair in enumerate(roots):
        jobs.append({'job': v, 'kind': 'selector', 'variable': v, 'edges': [(u, F(1)) for u in pair]})
        for u in pair: incoming[u] = v
    for v, sign, leaves, parents in trees:
        for p in parents:
            u = nodes[v, sign, p]
            for digit in range(k):
                cp, j = p + (digit,), len(jobs)
                row = {'job': j, 'kind': 'port' if len(cp) == h else 'edge', 'variable': v, 'sign': sign, 'parent': u}
                if len(cp) == h:
                    c = leaves[cp]
                    row.update(path=list(cp), clause=c, edges=[(u,F(1,k))] + [(bases[c]+z,F(1)) for z in range(min(capacities[c],degree[c]))], external={'start': bases[c], 'count': capacities[c], 'time': F(1)})
                    ports[c].append(j)
                else:
                    child = nodes[v, sign, cp]
                    row.update(child=child, edges=[(u,F(1,k)),(child,F(1))]); incoming[child] = j
                jobs.append(row); outgoing[u].append(j)
    assert len(jobs) == len(result['jobs']) == len(result['sigma'])
    assert roots == result['roots'] and internal == result['internal_machine_count']
    assert max(1,cursor) == result['full_machine_count'] and ranges == result['clause_ranges']
    load = Counter(); finite = 0
    for expected, actual, owner in zip(jobs, result['jobs'], result['sigma']):
        assert set(expected) == set(actual)
        for key, value in expected.items():
            if key == 'edges': assert [(u,F(p)) for u,p in actual[key]] == value
            elif key == 'external': assert {**actual[key], 'time': F(actual[key]['time'])} == value
            else: assert actual[key] == value
        edges = dict(expected['edges']); finite += len(edges)
        assert type(owner) is int and owner in edges
        load[owner] += edges[owner]
    listed = set(range(internal))
    for c,a in enumerate(capacities): listed.update(range(bases[c],bases[c]+min(a,degree[c])))
    if not cursor: listed.add(0)
    assert set(r['machine'] for r in result['listed_loads']) == listed
    for row in result['listed_loads']: assert load[row['machine']] == F(row['load'])
    assert max(load.values(),default=F(0)) == F(result['makespan']) <= F(result['bound']) == F(1)+F(k//2,k)
    assert all(value <= 1 for u,value in load.items() if u >= internal)
    assert F(result['omitted_unit_machine_load']) == 0
    assert result['omitted_unit_machine_count'] == sum(capacities)-sum(min(a,degree[c]) for c,a in enumerate(capacities))
    assert result['outgoing_jobs'] == {str(u): js for u,js in outgoing.items()}
    expected_slots, adj = [], [[] for _ in jobs]
    def slot(u, js):
        s=len(expected_slots); expected_slots.append({'slot':s,'machine':u,'jobs':js})
        for j in js: adj[j].append(s)
    for u in range(internal):
        order=[incoming[u]]+outgoing[u]
        for z in range(0,len(order),2):slot(u,order[z:z+2])
    for c,js in enumerate(ports):
        for z in range(0,len(js),2):slot(bases[c]+z//2,js[z:z+2])
    assert result['slots'] == expected_slots and result['job_slots'] == adj
    matching=result['matching']
    assert len(matching)==len(set(matching))==len(jobs)
    assert all(s in adj[j] and result['sigma'][j]==expected_slots[s]['machine'] for j,s in enumerate(matching))
    forest=result['forest']; r=(k+1)//2
    assert forest['r']==r and len(forest['variables'])==len(roots)
    selected_units, clause_count = [], Counter()
    for v, tree in enumerate(forest['variables']):
        assert tree['variable']==v and tree['root']==result['sigma'][v] in roots[v]
        active=set(tree['active_internal']); chosen=set(tree['selected_child_jobs']); selected_ports=set(tree['selected_ports'])
        assert len(active)==len(tree['active_internal'])==sum(r**depth for depth in range(h))
        assert len(chosen)==len(tree['selected_child_jobs'])==r*len(active)
        assert len(selected_ports)==len(tree['selected_ports'])==r**h
        assert tree['root'] in active
        assert all(incoming[u] in chosen for u in active if u!=tree['root'])
        assert all(len(chosen.intersection(outgoing[u]))==r for u in active)
        assert {j for j in chosen if jobs[j]['kind']=='port'}==selected_ports
        for j in chosen:
            job=jobs[j]; owner=result['sigma'][j]
            assert job['parent'] in active and owner != job['parent']
            if job['kind']=='edge':assert owner==job['child'] in active
            else:selected_units.append(owner);clause_count[job['clause']]+=1
    assert len(selected_units)==len(set(selected_units)) and sorted(selected_units)==forest['selected_unit_machines']
    assert [clause_count[c] for c in range(len(capacities))]==forest['selected_leaf_counts']
    return {'jobs':len(jobs),'finite_edges':finite,'listed_loads':len(listed),'slots':len(expected_slots),'forest_ports':len(selected_units),'makespan':result['makespan']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-dir',required=True);args=parser.parse_args()
    base,run=Path(__file__).resolve().parent,Path(args.run_dir).resolve();run.mkdir(parents=True,exist_ok=False)
    source=run/'source';shutil.copytree(base/'original',source)
    commands=[]
    def command(name,script,arguments=(),expected=0,environment=None):
        argv=[sys.executable,str(source/script),*map(str,arguments)]
        env=os.environ.copy();env.update(environment or {})
        p=subprocess.run(argv,capture_output=True,text=True,env=env)
        (run/(name+'.stdout')).write_text(p.stdout);(run/(name+'.stderr')).write_text(p.stderr)
        commands.append({'name':name,'argv':argv,'cwd':str(Path.cwd()),'environment_overrides':environment or {},'expected_exit_code':expected,'exit_code':p.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'})
        dump(run/'commands.json',commands);assert p.returncode==expected,name
        return p
    command('half-audit','unit_readout_half_density_three_halves.py',['--output',run/'half-audit.json'])
    half=json.loads((run/'half-audit.json').read_text());assert half['status']=='passed'
    sharp=half['sharp_reference']['input'];dump(run/'half-input.json',sharp)
    command('half-cli','unit_readout_half_density_three_halves.py',['--input',run/'half-input.json','--output',run/'half-cli.json'])
    first=json.loads((run/'half-cli.json').read_text())['result'];first_check=recheck(sharp,first)
    assert first['sigma']==half['sharp_reference']['sigma'] and first['listed_loads']==half['sharp_reference']['listed_loads']
    huge=10**5000+151
    giant={'k':1,'h':1,'variables':[{'id':0,'positive':[{'path':[0],'clause':0}],'negative':[{'path':[0],'clause':0}]}],'clause_capacities':[str(huge)]}
    dump(run/'giant-capacity-input.json',giant)
    failed=command('half-giant-default-limit','unit_readout_half_density_three_halves.py',['--input',run/'giant-capacity-input.json','--output',run/'giant-default-never-created.json'],expected=1,environment={'PYTHONINTMAXSTRDIGITS':'4300'})
    assert 'Exceeds the limit (4300 digits)' in failed.stderr and 'capacity_integer' in failed.stderr
    assert not (run/'giant-default-never-created.json').exists()
    command('half-giant-unlimited','unit_readout_half_density_three_halves.py',['--input',run/'giant-capacity-input.json','--output',run/'half-giant-unlimited.json'],environment={'PYTHONINTMAXSTRDIGITS':'0'})
    giant_result=json.loads((run/'half-giant-unlimited.json').read_text())['result'];giant_check=recheck(giant,giant_result)
    assert giant_result['full_machine_count']==huge+2
    command('selector-profile-audit','unit_readout_selector_profile_independent.py',['--output',run/'selector-profile-audit.json'])
    profile=json.loads((run/'selector-profile-audit.json').read_text());assert profile['status']=='passed'
    old=base.parent/'unit-readout-runtime/original/unit_readout_selector_mixing_sharp_profiles.json'
    old_data=json.loads(old.read_text())
    assert old_data=={'scope':profile['scope'],'certificates':profile['certificates']}
    report={'status':'passed-with-recorded-decimal-parser-boundary','python':platform.python_version(),'half_audit_counts':half['counts'],
            'sharp_half_literal_check':first_check,'giant_half_literal_check':giant_check,
            'giant_capacity_decimal_digits':len(str(huge)),'giant_capacity_bit_length':huge.bit_length(),
            'default_limit_failure_recorded':True,'unlimited_environment_success':True,
            'profile_totals':profile['totals'],'profile_checks':profile['checks'],
            'profile_certificates_equal_previous_frozen_json':True,'previous_frozen_profile_sha256':sha256(old.read_bytes()).hexdigest(),
            'commands':commands,'source_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted((base/'original').iterdir()) if p.is_file()},
            'scope':'Two new original programs only. Half-density audit, new sharp CLI and decimal parser boundary; no SAT/LP/OPT oracle. Two CLI schedules/slots/forests rechecked without original imports. Independent p1..4 profile generator checked its serialized full matrices; its exact certificates equal the previously frozen JSON, which was not regenerated by an old entrypoint.'}
    dump(run/'verification.json',report)
    print(json.dumps({'status':report['status'],'half_counts':report['half_audit_counts'],'profile_totals':report['profile_totals']},ensure_ascii=False))


if __name__=='__main__':main()
