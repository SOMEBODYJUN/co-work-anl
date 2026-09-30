#!/usr/bin/env python3
"""Reproducible direct certificate and independent support-enumeration audit."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import json
import random
import time
from r_menu_solver import solve,make_menu,serial,verify

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('support_oracle',ROOT/'astra_ring'/'mitm_solver.py')
oracle=importlib.util.module_from_spec(spec);spec.loader.exec_module(oracle)


def exact_optimum(instance):
    weights=[Q(str(v)) for v in instance['weights']]
    sites=[set(v) for v in instance['locations']]
    pairs={};d1={};d2={}
    for s in instance['U1']:
        for t in instance['U2']:
            ws=[weights[i] for i in sorted(sites[s]&sites[t])]
            a=sum((weights[i] for i in sites[s]-sites[t]),Q(0))
            b=sum((weights[i] for i in sites[t]-sites[s]),Q(0))
            total=a+b+sum(ws,Q(0))
            mingap=oracle.brute_pair(a,b,ws)[1]
            maxgap=oracle.brute_pair(a,b,ws,target=total,score=lambda z:-z)[1]
            m1=(total+mingap)/2;m2=(total-maxgap)/2
            d1[t]=max(d1.get(t,Q(0)),m1);d2[s]=max(d2.get(s,Q(0)),m2)
            menu=make_menu(weights,sites,s,t)
            assert min(e['loads'][0] for e in menu['entries'])>=m1
            assert min(e['loads'][1] for e in menu['entries'])>=m2
            pairs[s,t]=(a,b,ws,total)
    best=None
    for (s,t),(a,b,ws,total) in pairs.items():
        den=d1[t]+d2[s]
        target=total*(d1[t]-d2[s])/den if den else Q(0)
        def score(gap):
            x=(total+gap)/2;y=(total-gap)/2
            if (not x and d1[t]) or (not y and d2[s]):
                return Q(10**30)
            return max(Q(1),d1[t]/x if x else Q(0),d2[s]/y if y else Q(0))
        value=oracle.brute_pair(a,b,ws,target=target,score=score)[0]
        best=value if best is None else min(best,value)
    return best


def main():
    rng=random.Random(2026093011)
    records={'seed_mode':'maximum_only','seed':2026093011,'random_certificate_checks':0,'support_comparisons':0,
             'directed_checks':0,'four_cycles':0,'largest_reported_factor':'1',
             'general_seed':63231,'general_catalog_certificate_checks':0,
             'general_four_cycles':0,'general_cycles_at_least_six':0,
             'maximum_observed_cycle_length':0}
    maximum=Q(1);start=time.time()
    directed=[
        {'weights':[],'locations':[[],[],[]],'U1':[0,1],'U2':[2]},
        {'weights':[1],'locations':[[0],[0]],'U1':[0,1],'U2':[0,1]},
        {'weights':[1,2,4],'locations':[[0,1,2],[1,2],[],[0]],'U1':[0,2],'U2':[1,3]},
        {'weights':['44504187','35689587','1','80193774','100000000','44504185'],
         'locations':[[0,4],[1,5],[2,4,5],[3,4]],'U1':[0,1],'U2':[2,3]},
    ]
    for case in directed:
        out=solve(case);assert out['alpha']>=exact_optimum(case)
        records['directed_checks']+=1
        maximum=max(maximum,out['alpha'])
    for number in range(500):
        n=rng.randint(0,10);large=rng.randint(1,6)
        small=rng.randint(1,2);count=small+large
        weights=[str(Q(rng.randint(1,60),rng.randint(1,17))) for _ in range(n)]
        sites=[[i for i in range(n) if rng.randrange(4)<rng.randint(1,3)] for _ in range(count)]
        u1=list(range(small));u2=list(range(small,count))
        if number%5==0:
            u2=list(range(count)) # overlapping physical catalogs
        if number%2:
            u1,u2=u2,u1 # both orientations of the small catalog
        case={'weights':weights,'locations':sites,'U1':u1,'U2':u2}
        out=solve(case);verify(case,json.loads(json.dumps(serial(out))))
        records['random_certificate_checks']+=1
        records['four_cycles']+=len(out['response_cycle'])==4
        maximum=max(maximum,out['alpha'])
        if n<=5 and number<250:
            assert exact_optimum(case)<=out['alpha']
            records['support_comparisons']+=1
    general_rng=random.Random(records['general_seed'])
    saved_long_cycle=False
    for number in range(1500):
        a=general_rng.randint(3,7);b=general_rng.randint(3,7);n=general_rng.randint(2,15)
        weights=[str(Q(general_rng.randint(1,60),general_rng.randint(1,20))) for i in range(n)]
        sites=[[i for i in range(n) if general_rng.random()<.5] for j in range(a+b)]
        case={'weights':weights,'locations':sites,'U1':list(range(a)),'U2':list(range(a,a+b))}
        out=solve(case)
        verify(case,json.loads(json.dumps(serial(out))))
        records['general_catalog_certificate_checks']+=1
        length=len(out['response_cycle'])
        records['general_four_cycles']+=length==4
        records['general_cycles_at_least_six']+=length>=6
        records['maximum_observed_cycle_length']=max(records['maximum_observed_cycle_length'],length)
        maximum=max(maximum,out['alpha'])
        if length>=6 and not saved_long_cycle:
            destination=Path(__file__).with_name('r_menu_six_cycle_example.json')
            destination.write_text(json.dumps({'instance':case,'certificate':serial(out)},indent=2)+'\n')
            saved_long_cycle=True
    damaged=solve(directed[-1]);damaged['on_path']['prob_first'][0]=1-damaged['on_path']['prob_first'][0]
    try:
        verify(directed[-1],damaged)
    except AssertionError:
        records['corrupted_certificate_rejected']=True
    else:
        raise AssertionError('corrupted certificate accepted')
    records['largest_reported_factor']=str(maximum)
    records['elapsed_seconds']=round(time.time()-start,3)
    destination=Path(__file__).with_name('r_menu_verification.json')
    destination.write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':
    main()
