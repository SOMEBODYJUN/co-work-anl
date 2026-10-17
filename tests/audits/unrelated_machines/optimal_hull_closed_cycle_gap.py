#!/usr/bin/env python3
"""Exact finite audit of positive closed evacuation cycles. Finite audit only; default stdout does not overwrite evidence."""
from fractions import Fraction as F
from itertools import product
from math import ceil
import json, sys, platform

def build(k,d):
    if isinstance(k,bool) or not isinstance(k,int) or k<3 or isinstance(d,bool) or not isinstance(d,int) or d<1:
        raise ValueError("integer k>=3,d>=1 required")
    b=a=F(k-1,k); delta=F(k-1,k*k); c=F(1,k*k); beta=F(1,k)
    D=d+k-1
    chains=[]; jobs=[]; P={}; machines=['r']
    for t in range(k+1):
        h=D if t==k else d
        g=f'g{t}'
        homes=[f'h{t}_{u}' for u in range(h)]
        es=[f'e{t}_{u}' for u in range(h)]
        machines+=homes
        P[g]={'r':b if t==k else (delta+c/4 if t==0 else delta),homes[0]:F(1)};jobs.append(g)
        for u,e in enumerate(es):
            P[e]={homes[u]:a,(homes[u+1] if u+1<h else 'r'):(F(1) if u+1<h else (c/2 if t==0 else c))};jobs.append(e)
        chains.append((g,homes,es))
    def activate(subset):
        out={}
        for t,(g,hs,es) in enumerate(chains):
            active=t in subset
            out[g]=hs[0] if active else 'r'
            for u,e in enumerate(es):out[e]=(hs[u+1] if u+1<len(hs) else 'r') if active else hs[u]
        return out
    S0=activate(set(range(k)));S1=activate({k});bad=activate({0})
    x={j:{} for j in jobs}
    for j in jobs:
        for i in P[j]:x[j][i]=beta*(S0[j]==i)+(1-beta)*(S1[j]==i)
    # Perturbed processing times force t0 first among tinies and its tail last.
    # Remaining equal-time ties may be resolved by the ordinary input order.
    tail0=chains[0][2][-1]
    index={j:u for u,j in enumerate(jobs)}
    def tie(j):return index[j]
    slots={}; edges={j:[] for j in jobs}; intervals={}
    for i in machines:
        order=sorted((j for j in jobs if x[j].get(i,0)>0),key=lambda j:(-P[j][i],tie(j)))
        cur=F(0)
        for j in order:
            end=cur+x[j][i];intervals[i,j]=(cur,end)
            for s in range(cur.numerator//cur.denominator,ceil(end)):
                if max(cur,F(s))<min(end,F(s+1)):edges[j].append((i,s))
            cur=end
        slots[i]=ceil(cur)
    return locals()

def loads(z,s):
    out={i:F(0) for i in z['machines']}
    for j,i in s.items():out[i]+=z['P'][j][i]
    return out

def slot_witness(z,s):
    # Independent augmenting matcher restricted to assignment s.
    matched={}
    def augment(j,seen):
        for slot in z['edges'][j]:
            if slot[0]!=s[j] or slot in seen:continue
            seen.add(slot)
            if slot not in matched or augment(matched[slot],seen):matched[slot]=j;return True
        return False
    if all(augment(j,set()) for j in z['jobs']):return {j:slot for slot,j in matched.items()}
    return None

def literal_slot_matchings(z):
    order=sorted(z['jobs'],key=lambda j:(len(z['edges'][j]),j))
    chosen={};used=set();total=0;minimum=None;min_count=0;min_assignments=set()
    def visit(t,cost):
        nonlocal total,minimum,min_count,min_assignments
        if t==len(order):
            total+=1
            assignment=tuple(chosen[j][0] for j in z['jobs'])
            if minimum is None or cost<minimum:
                minimum=cost;min_count=1;min_assignments={assignment}
            elif cost==minimum:
                min_count+=1;min_assignments.add(assignment)
            return
        j=order[t]
        for slot in z['edges'][j]:
            if slot not in used:
                used.add(slot);chosen[j]=slot
                visit(t+1,cost+z['P'][j][slot[0]])
                used.remove(slot);del chosen[j]
    visit(0,F(0))
    assert min_assignments=={tuple(z['bad'][j] for j in z['jobs'])}
    return {'literal_slot_matchings':total,'literal_minimum_slot_matchings':min_count,
            'literal_minimum_cost':str(minimum),'literal_minimum_machine_assignments':len(min_assignments)}

def single_job_escape(z):
    s=dict(z['bad']);B=max(loads(z,s).values());c=z['c']
    first_peaks=[]
    for j in z['jobs']:
        t=dict(s);t[j]=next(i for i in z['P'][j] if i!=s[j])
        first_peaks.append(max(loads(z,t).values()))
    assert min(first_peaks)==B+c
    peak=B;steps=0
    for q in range(1,z['k']):
        g,hs,es=z['chains'][q]
        for u in range(len(es)-1,-1,-1):
            s[es[u]]=hs[u+1] if u+1<len(hs) else 'r'
            peak=max(peak,max(loads(z,s).values()));steps+=1
        s[g]=hs[0];peak=max(peak,max(loads(z,s).values()));steps+=1
    assert s==z['S0'] and peak==B+c and steps==(z['k']-1)*(z['d']+1)
    return {'steps_to_optimum':steps,'minimum_first_move_peak':str(min(first_peaks)),
            'path_peak':str(peak),'excess_over_bad':str(c)}

def audit(k,d):
    z=build(k,d);jobs=z['jobs'];P=z['P'];m=len(z['machines']);n=len(jobs)
    B=2-F(3,k)+F(3,2*k*k);ct=F(d,k)+z['c']-z['delta'];ct0=F(d,k)-z['delta']+z['c']/4;cb=F(z['D'],k)+z['c']-z['b']
    assert ct0>0 and ct-ct0==3*z['c']/4 and cb-ct==z['delta']
    assert n==(k+1)*d+2*k and m==(k+1)*d+k
    assert max(loads(z,z['S0']).values())==1 and max(loads(z,z['S1']).values())==1
    assert max(loads(z,z['bad']).values())==B
    assert all(sum(P[j][i]*z['x'][j].get(i,0) for j in jobs if i in P[j])<=1 for i in z['machines'])
    assert sum(z['slots'].values())==n
    assert slot_witness(z,z['bad']) is not None
    # Explicit bad slot injection, no augmenting-matcher oracle.
    explicit={z['chains'][k][0]:('r',0),z['tail0']:('r',k)}
    for t in range(1,k):explicit[z['chains'][t][0]]=('r',t)
    for t,(g,hs,es) in enumerate(z['chains']):
        if t==0:
            explicit[g]=(hs[0],0)
            for u,e in enumerate(es[:-1]):explicit[e]=(hs[u+1],0)
        else:
            for u,e in enumerate(es):explicit[e]=(hs[u],0)
    assert len(explicit)==n and len(set(explicit.values()))==n
    assert all(slot in z['edges'][j] for j,slot in explicit.items())
    assert all(z['bad'][j]==slot[0] for j,slot in explicit.items())
    optimum=None;nontrivial=0;minjobs=n+1;minmachines=m+1;minimum_slot_cost=None;slot_schedules=0;minimum_slot_count=0;minimum_slot_schedules=[]
    all_options=[list(P[j]) for j in jobs]
    best_examples=[]
    for choices in product(*all_options):
        s=dict(zip(jobs,choices));ls=loads(z,s);C=max(ls.values())
        optimum=C if optimum is None else min(optimum,C)
        changed=[j for j in jobs if s[j]!=z['bad'][j]]
        if C<=B and changed:
            nontrivial+=1;mv={i for j in changed for i in (s[j],z['bad'][j])}
            if len(changed)<minjobs:minjobs=len(changed);best_examples=[changed]
            minmachines=min(minmachines,len(mv))
        wit=slot_witness(z,s)
        if wit is not None:
            slot_schedules+=1;cost=sum(ls.values())
            if minimum_slot_cost is None or cost<minimum_slot_cost:
                minimum_slot_cost=cost;minimum_slot_count=1;minimum_slot_schedules=[s]
            elif cost==minimum_slot_cost:
                minimum_slot_count+=1;minimum_slot_schedules.append(s)
    assert optimum==1 and minjobs==d+1 and minmachines==d+1
    assert minimum_slot_count==1 and minimum_slot_schedules==[z['bad']]
    good=z['activate']({0,1});assert max(loads(z,good).values())==B-z['delta']+z['c']
    assert sum(good[j]!=z['bad'][j] for j in jobs)==d+1
    return {'k':k,'d':d,'m':m,'n':n,'legal_assignments':2**n,'opt':str(optimum),'bad_makespan':str(B),'weak_feasible_nontrivial_assignments':nontrivial,'min_changed_jobs':minjobs,'min_participating_machines':minmachines,'slot_supported_schedules':slot_schedules,'minimum_slot_cost':str(minimum_slot_cost),'minimum_slot_assignment_count':minimum_slot_count,'first_tiny_activation_cost':str(ct0),'other_tiny_activation_cost':str(ct),'macro_activation_cost':str(cb),'tail0_root_interval':[str(v) for v in z['intervals']['r',z['tail0']]],'single_job_escape':single_job_escape(z),'literal_slot_enumeration':literal_slot_matchings(z)}

if __name__=='__main__':
    pairs=[(3,1),(3,2),(4,1)]
    print(json.dumps({'python':platform.python_version(),'arithmetic':'fractions.Fraction','scope':'All labelled legal two-choice assignments; independent within-assignment slot augmenting matching; finite evidence only','runs':[audit(*v) for v in pairs]},indent=2))
