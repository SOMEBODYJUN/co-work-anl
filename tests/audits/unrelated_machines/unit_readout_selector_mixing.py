#!/usr/bin/env python3
"""Private unit-readout trees: complete-YES-supported prescribed selector mixing.

Reuses the reviewed original-P builder, exact load checker and generic Hall
matching of unit_readout_calibrated_cardinality.py. This is not an independent
implementation of those helpers. Inactive-rail jobs are FIXED at their parents;
they are not subjected to the strong calibrated LP row budget.

Input JSON: {"instance": <existing explicit leaf schema>,
             "yes_schedules": [[machine for every original job],...],
             "prescribed_signs": [0 or 1 for every variable]}.
Every supplied schedule is checked as an actual complete C<=1 schedule first.
Unit names within a clause are then canonically compressed to the first
min(A,d) interchangeable original units. For p=1 this normalized original
witness is returned directly, with no mixing/LP/OPT computation.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json
import sys
if hasattr(sys,'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)
import unit_readout_calibrated_cardinality as core

SOURCE_CLAIMS=('UM-UNIT-READOUT-SELECTOR-MIXING-v1',)


def validate_and_normalize_yes(I,sigma):
    if type(sigma) not in (list,tuple): raise ValueError('explicit complete YES sigma list required')
    sigma=list(sigma); loads=core.actual_loads(I,sigma)
    if max(loads.values(),default=F(0))>1: raise ValueError('supplied actual YES exceeds C=1')
    signs=[]
    for v,roots in enumerate(I['roots']):
        if sigma[v] not in roots: raise ValueError('selector has unavailable root')
        signs.append(roots.index(sigma[v]))
    # All selected tree jobs must down-propagate under a true C<=1 schedule.
    selected_counts=[0]*len(I['A'])
    for j,job in enumerate(I['jobs']):
        if job['kind']=='selector' or job['sign']!=signs[job['variable']]: continue
        if job['kind']=='edge':
            if sigma[j]!=job['child']: raise RuntimeError('actual C1 failed full-tree propagation')
        else:
            if sigma[j]==job['parent']: raise RuntimeError('actual C1 failed full-leaf readout')
            selected_counts[job['clause']]+=1
    if any(d>a for d,a in zip(selected_counts,I['A'])): raise RuntimeError('selected full trees exceed actual C1 clause capacity')
    normalized=list(sigma); renamings=[]
    for c,ports in enumerate(I['clause_ports']):
        used=sorted({sigma[j] for j in ports if sigma[j]!=I['jobs'][j]['parent']})
        if len(used)>I['ranges'][c]['listed_units']: raise RuntimeError('too many actual C1 unit hosts')
        mapping={u:I['ranges'][c]['start']+i for i,u in enumerate(used)}
        for j in ports:
            if sigma[j]!=I['jobs'][j]['parent']: normalized[j]=mapping[sigma[j]]
        renamings.append({'clause':c,'old_to_new':[[u,mapping[u]] for u in used if u!=mapping[u]]})
    if max(core.actual_loads(I,normalized).values(),default=F(0))>1: raise RuntimeError('unit renaming changed C1 feasibility')
    return normalized,signs,selected_counts,renamings


def construct_selector_mixing(data,yes_schedules,prescribed_signs):
    I=core.build_instance(data)
    if type(yes_schedules) not in (list,tuple) or not yes_schedules: raise ValueError('at least one explicit complete YES schedule required')
    if type(prescribed_signs) not in (list,tuple) or len(prescribed_signs)!=len(I['roots']) or any(type(s) is not int or s not in (0,1) for s in prescribed_signs): raise ValueError('one exact 0/1 prescribed sign per variable required')
    prescribed=list(prescribed_signs); p=len(yes_schedules); checked=[validate_and_normalize_yes(I,sigma) for sigma in yes_schedules]
    for v,s in enumerate(prescribed):
        if all(record[1][v]!=s for record in checked): raise ValueError('prescribed selector sign not covered by supplied actual YES')
    metadata={'source_claims':SOURCE_CLAIMS,'p':p,'prescribed_signs':prescribed,'input_yes_selector_signs':[record[1] for record in checked],'input_yes_selected_leaf_counts':[record[2] for record in checked],'input_yes_unit_renamings':[record[3] for record in checked],'uniform_profile_bound':F(2)-F(1,2*p-1)}
    if not I['roots']:
        return core.finish(I,[],F(0),mode='selector-mixing-empty',leaf_count=None,**metadata)
    # Explicit leaves supply N, avoiding binary exponent expansion altogether.
    N=len(I['trees'][0][0]['wiring'])
    if N<p: raise ValueError('nonempty mixing contract requires N=k^h>=p')
    if p==1:
        return core.finish(I,checked[0][0],F(1),mode='selector-mixing-one-YES',leaf_count=N,r=I['k'],**metadata)
    k=I['k']; r=k//p if k>=p else 1
    x=[F(1)]
    for depth in range(I['h']): x.append((r-1+x[-1])/k)
    if x[-1]>F(1,p): raise RuntimeError('prescribed active calibration exceeds 1/p')
    jobs=I['jobs']; selected_counts=[0]*len(I['A']); active_machines=[]
    for u in range(I['internal_count']):
        job=jobs[I['outgoing'][u][0]]
        if job['sign']==prescribed[job['variable']]: active_machines.append(u)
    moving=[j for j,job in enumerate(jobs) if job['kind']=='selector' or job['sign']==prescribed[job['variable']]]
    local_index={j:i for i,j in enumerate(moving)}; rows={}; column=Counter()
    def put(j,u,mass):
        if mass:
            row=rows.setdefault(u,{})
            row[j]=row.get(j,F(0))+mass; column[j]+=mass
    for j in moving:
        job=jobs[j]
        if job['kind']=='selector': put(j,I['roots'][job['variable']][prescribed[job['variable']]],F(1))
        else:
            t=x[len(job['path'])]; put(j,job['parent'],1-t)
            if job['kind']=='edge': put(j,job['child'],t)
            else: selected_counts[job['clause']]+=1
    covered_counts=[sum(record[2][c] for record in checked) for c in range(len(I['A']))]
    if any(d>u or u>p*a for d,u,a in zip(selected_counts,covered_counts,I['A'])): raise RuntimeError('complete-YES leaf coverage count failed')
    clause_mass=[]
    for c,ports in enumerate(I['clause_ports']):
        total=selected_counts[c]*x[-1]; clause_mass.append(total)
        if total>I['A'][c]: raise RuntimeError('selected clause mass exceeds original capacity')
        unit=0; filled=F(0)
        for j in ports:
            if j not in local_index: continue
            mass=x[-1]
            while mass:
                if unit>=I['ranges'][c]['listed_units']: raise RuntimeError('clipped unit range insufficient')
                take=min(mass,1-filled); put(j,I['ranges'][c]['start']+unit,take); mass-=take; filled+=take
                if filled==1: unit+=1; filled=F(0)
    if any(column[j]!=1 for j in moving): raise RuntimeError('moving job fractional column not exactly one')
    slots=[]; adj=[[] for j in moving]; B=k-r+1
    def add_row(u,ordered):
        local=[]; position=F(0)
        for j in ordered:
            mass=rows.get(u,{}).get(j,F(0))
            while mass:
                index=position.numerator//position.denominator
                if index==len(local):
                    s=len(slots); local.append(s); slots.append({'slot':s,'machine':u,'fractions':[]})
                s=local[index]; take=min(mass,F(index+1)-position); slots[s]['fractions'].append([j,take])
                if s not in adj[local_index[j]]: adj[local_index[j]].append(s)
                position+=take; mass-=take
        return local,position
    row_cardinality=[]
    for u in active_machines:
        local,mass=add_row(u,[I['incoming'][u]]+I['outgoing'][u])
        if mass>B or len(local)>B: raise RuntimeError('active integer row-cardinality budget exceeded')
        row_cardinality.append({'machine':u,'mass':mass,'slots':len(local)})
    for u,row in sorted(rows.items()):
        if u>=I['internal_count']:
            local,mass=add_row(u,sorted(row))
            if mass>1 or len(local)>1: raise RuntimeError('external unit fraction overloaded')
    slot_columns=Counter()
    for slot in slots:
        if not 0<sum((mass for j,mass in slot['fractions']),F(0))<=1: raise RuntimeError('invalid slot mass')
        for j,mass in slot['fractions']: slot_columns[j]+=mass
    if any(slot_columns[j]!=1 for j in moving): raise RuntimeError('slot job column not one')
    matched=core.covering_matching(adj,len(slots))
    sigma=[None if job['kind']=='selector' else job['parent'] for job in jobs]
    for j,s in zip(moving,matched): sigma[j]=slots[s]['machine']
    for v,s in enumerate(prescribed):
        if sigma[v]!=I['roots'][v][s]: raise RuntimeError('matching violated prescribed selector')
    for j,job in enumerate(jobs):
        if j not in local_index and sigma[j]!=job['parent']: raise RuntimeError('inactive tree job not fixed at parent')
    bound=F(2)-F(r,k)
    if bound>metadata['uniform_profile_bound']: raise RuntimeError('profile constant 2-1/(2p-1) missed')
    return core.finish(I,sigma,bound,mode='selector-mixing-calibrated-active-only',leaf_count=N,r=r,x_by_depth=x,selected_leaf_arity=selected_counts,clause_fractional_mass=clause_mass,active_internal_row_cardinality=row_cardinality,moving_jobs=moving,moving_job_slots=adj,moving_matching=matched,slots=slots,**metadata)


def strict_schedule(data,signs,use_last_units=False):
    """Audit fixture only: all selected trees fully down, inactive all parent."""
    I=core.build_instance(data); sigma=[None if job['kind']=='selector' else job['parent'] for job in I['jobs']]; selected_ports=[[] for a in I['A']]
    for v,s in enumerate(signs): sigma[v]=I['roots'][v][s]
    for j,job in enumerate(I['jobs']):
        if job['kind']=='selector' or job['sign']!=signs[job['variable']]: continue
        if job['kind']=='edge': sigma[j]=job['child']
        else: selected_ports[job['clause']].append(j)
    for c,ports in enumerate(selected_ports):
        if len(ports)>I['A'][c]: raise ValueError('fixture selected full trees exceed clause capacity')
        shift=I['A'][c]-len(ports) if use_last_units else 0
        for t,j in enumerate(ports): sigma[j]=I['ranges'][c]['start']+shift+t
    if max(core.actual_loads(I,sigma).values(),default=F(0))>1: raise RuntimeError('invalid strict audit fixture')
    return sigma


def one_hot_instance(p,k,h,aux_dead=False,huge=False):
    N=k**h; V=p+int(aux_dead); A=[N]*(p+1)
    wiring=[]
    for v in range(p): wiring.extend([0]*N+[v+1]*N)
    if aux_dead:
        wiring.extend([p+1]*N+[p+2]*N); A.extend([N,0])
    if huge: A=[a+10**100+151 if a else a for a in A]
    data=core.encode(V,k,h,wiring,A); yes=[]
    for chosen in range(p):
        signs=[1]*p; signs[chosen]=0
        if aux_dead: signs.append(0)
        yes.append(strict_schedule(data,signs,use_last_units=huge))
    return data,yes,[0]*V


def audit():
    import hashlib,time
    start=time.perf_counter(); counts=Counter(); certificates=[]
    def direct_check(result):
        loads=Counter()
        for job,u in zip(result['jobs'],result['sigma']):
            finite=dict(job['edges'])
            if u in finite: value=finite[u]
            elif job['kind']=='port' and job['external']['start']<=u<job['external']['start']+job['external']['count']: value=F(1)
            else: raise AssertionError('actual original edge unavailable')
            loads[u]+=value
        assert len(result['jobs'])==len(result['sigma'])
        assert max(loads.values(),default=F(0))==result['makespan']<=result['bound']
        assert all(loads[row['machine']]==row['load'] for row in result['listed_loads'])
        assert all(result['sigma'][v]==roots[s] for v,(roots,s) in enumerate(zip(result['roots'],result['prescribed_signs'])))
        counts['actual_complete_schedules']+=1; counts['actual_jobs']+=len(result['jobs']); counts[result['mode']]+=1
    for p,k,h,dead,huge in ((2,3,1,False,False),(3,5,1,False,False),(2,4,2,True,False),(3,2,2,False,False),(1,2,1,True,True),(1,1,35,True,False)):
        data,yes,prescribed=one_hot_instance(p,k,h,dead,huge); result=construct_selector_mixing(data,yes,prescribed); direct_check(result)
        if (p,k,h) in ((2,3,1),(3,5,1)):
            # Conditional profile lower bound: k=2p-1 units cannot give >=2
            # external leaves to all p prescribed positive roots. Some root
            # retains >=k-1 small jobs, hence C>=2-1/k; result attains it.
            assert k==2*p-1 and result['makespan']==F(2)-F(1,k)==result['uniform_profile_bound']
            counts['sharp_profile_capacity_lower_bounds']+=1
        certificates.append({'instance':data,'yes_schedules':yes,'prescribed_signs':prescribed,'result':result})
    empty={'k':10**100,'h':10**100,'variables':[],'clause_capacities':[0,10**100+151]}
    result=construct_selector_mixing(empty,[[],[]],[]); direct_check(result); assert result['leaf_count'] is None
    data,yes,prescribed=one_hot_instance(2,3,1)
    bad=[('incomplete',data,[yes[0][:-1],yes[1]],prescribed),('no-witness',data,[],prescribed),('uncovered',data,[yes[0]],[1,0]),('bad-sign-type',data,yes,[True,0])]
    overloaded=list(yes[0]); I=core.build_instance(data)
    # Put every job at parent, including selected root's k outgoing: C=2.
    overloaded=[I['roots'][job['variable']][0] if job['kind']=='selector' else job['parent'] for job in I['jobs']]
    bad.append(('not-C1',data,[overloaded],prescribed))
    unary,unary_yes,unary_p=one_hot_instance(1,1,1)
    bad.append(('N<p',unary,unary_yes*2,unary_p))
    for name,instance,witnesses,signs in bad:
        try: construct_selector_mixing(instance,witnesses,signs)
        except ValueError: counts['rejected_invalid_'+name]+=1
        else: raise AssertionError('invalid input accepted: '+name)
    return {'status':'passed','source_claims':SOURCE_CLAIMS,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reused_core_sha256':hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),'counts':dict(counts),'full_original_certificates':certificates,'scope':'Targeted actual original-job qualification/load and fixed-selector checks, two exact conditional-profile sharp examples. No generic LP/OPT solver or exhaustive-search production. Reuses reviewed builder/matching; not an independent implementation.','elapsed_seconds':time.perf_counter()-start}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--input'); parser.add_argument('--output'); args=parser.parse_args()
    if args.input:
        payload=json.loads(Path(args.input).read_text())
        if type(payload) is not dict or set(payload)!={'instance','yes_schedules','prescribed_signs'}: raise ValueError('exact mixing payload keys required')
        result=construct_selector_mixing(payload['instance'],payload['yes_schedules'],payload['prescribed_signs'])
    else: result=audit()
    output=json.dumps(core.jsonable(result),ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with Path(args.output).open('x') as handle: handle.write(output)
    else: sys.stdout.write(output)
