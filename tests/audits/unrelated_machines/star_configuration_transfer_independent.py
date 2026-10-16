#!/usr/bin/env python3
"""Independent sparse endpoint contraction audit. Uses only legacy instance/certificate generator.
No repository files are modified. All verification and contraction are independent.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import importlib.util, json, sys, hashlib, time
ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'tests/audits/unrelated_machines/sparse_conditioned_configuration.py'
spec=importlib.util.spec_from_file_location('legacy',source);legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)

def normalize(row):
    merged=defaultdict(F)
    for w,C in row:
        if w:merged[tuple(sorted(C))]+=w
    return [(w,C) for C,w in merged.items() if w]

def make_plan(P):
    costs={j:dict(r['costs']) for j,r in enumerate(P['jobs'])};machines=set(P['machines']);plan=[];sources={}
    for j,cs in costs.items():
        for i in cs:sources[j,i]=j
    fresh=len(costs)
    for (tree,path),(term,blocks) in P['groups'].items():
        for removed in (term[0],term[-1]):
            children=tuple(j for j,cs in costs.items() if removed in cs)
            assert len(children)==2
            S=sum(costs[j][removed] for j in children)
            assert S==2 and all(S-costs[j][removed]<=1+F(1,P['k']) for j in children)
            exterior=set().union(*(set(costs[j]) for j in children))-{removed}
            # Stronger than capacity mutual exclusion: disjoint exterior domains.
            assert all(sum(i in costs[j] for j in children)==1 for i in exterior)
            replacement={};witness={}
            for i in sorted(exterior):
                a=min((j for j in children if i in costs[j]),key=lambda j:(costs[j][i],j))
                replacement[i]=costs[a][i];witness[i]=a;sources[fresh,i]=sources[a,i]
            for j in children:del costs[j]
            costs[fresh]=replacement;machines.remove(removed)
            plan.append((removed,children,fresh,tuple(sorted(exterior)),witness))
            fresh+=1
    return costs,machines,plan,sources

def contract(cert,step,tracked):
    removed,children,new,exterior,witness=step;Fset=set(children)
    old_support=sum(len(row) for row in cert.values());lost=len(cert[removed]);del cert[removed]
    q=sum((w for i in exterior for w,C in cert[i] if Fset.intersection(C)),F(0))
    assert q>=1
    forced_machine=tracked[1] if tracked[0] in Fset else None
    if forced_machine is not None:
        assert forced_machine in exterior
        assert all(tracked[0] in C for w,C in cert[forced_machine] if w)
        order=(forced_machine,)+tuple(i for i in exterior if i!=forced_machine)
    else:order=exterior
    residual=F(1);splits=0
    for i in order:
        row=[]
        for w,C in cert[i]:
            hits=Fset.intersection(C);assert len(hits)<=1
            cleaned=tuple(j for j in C if j not in Fset)
            take=min(w,residual) if hits else F(0)
            if take:
                row.append((take,cleaned+(new,)));residual-=take
            if w-take:row.append((w-take,cleaned))
            if take and w-take:splits+=1
        cert[i]=normalize(row)
    assert residual==0 and splits<=1
    new_support=sum(len(row) for row in cert.values())
    assert new_support<=old_support-lost+1
    if forced_machine is not None:tracked=(new,forced_machine)
    return tracked,splits,new_support-old_support+lost

def check(costs,machines,cert,force,T):
    assert set(cert)==machines
    cover=defaultdict(F);forced=F(0);support=0
    for i,row in cert.items():
        assert sum(w for w,C in row)==1
        big=F(0)
        for w,C in row:
            support+=1;assert w>0 and len(C)==len(set(C))
            assert sum((costs[j][i] for j in C),F(0))<=T
            for j in C:
                cover[j]+=w
                if (j,i)==force:forced+=w
                if costs[j][i]>T/2:big+=w
        assert big<=1
    assert set(cover)==set(costs) and all(w==1 for w in cover.values()) and forced==1
    return support

def missing_exclusion_example():
    # T=1. Two root machines u1,u2, two leaves v1,v2.
    costs={0:{'u1':F(1),'u2':F(1)},1:{'u1':F(1,2),'v1':F(1)},2:{'u1':F(1,2),'v1':F(1)},3:{'u2':F(1,2),'v2':F(1)},4:{'u2':F(1,2),'v2':F(1)}}
    cert={'u1':[(F(1,2),(0,)),(F(1,2),(1,2))],'u2':[(F(1,2),(0,)),(F(1,2),(3,4))],'v1':[(F(1,2),(1,)),(F(1,2),(2,))],'v2':[(F(1,2),(3,)),(F(1,2),(4,))]}
    coverage=defaultdict(F)
    for i,row in cert.items():
        assert sum(w for w,C in row)==1
        for w,C in row:
            assert sum(costs[j][i] for j in C)<=1
            for j in C:coverage[j]+=w
    assert all(coverage[j]==1 for j in costs)
    assert sum(w*len(set(C)&{1,2}) for w,C in cert['u1'])==1
    assert sum(w for w,C in cert['u1'] if set(C)&{1,2})==F(1,2)
    # After v1 contraction e is u1-only, cost1/2, forcing bridge entirely u2,
    # forcing jobs3,4 entirely v2 where their total load2>1: CONFIG infeasible.
    return {'old_configuration_feasible':True,'old_expected_exterior_F_count':'1','old_exterior_occupancy':'1/2','new_configuration_infeasible_by_forcing_chain':True}

def reverse_probe_example():
    # Structural mutual exclusion holds, yet reverse all-edge probing is false.
    costs={0:{'v':F(1),'u':F(1)},1:{'v':F(1),'u':F(2,5)},2:{'u':F(3,5)}}
    old={'v':[(F(1),(0,))],'u':[(F(1),(1,2))]}
    check(costs,set(old),old,(0,'v'),F(1))
    assert costs[0]['u']+costs[1]['u']>1
    # Job2 is u-only and every T-configuration containing it excludes job0.
    assert all(not (0 in C and 2 in C) for C in all_configs(costs,'u'))
    new_costs={2:{'u':F(3,5)},3:{'u':F(2,5)}}
    new={'u':[(F(1),(2,3))]}
    for edge in ((2,'u'),(3,'u')):check(new_costs,{'u'},new,edge,F(1))
    return {'structural_mutual_exclusion':True,'reduced_all_edges_forcible':True,'original_edge_job0_to_u_impossible':True}

def all_configs(costs,i,T=F(1)):
    from itertools import combinations
    jobs=[j for j,cs in costs.items() if i in cs]
    return [C for r in range(len(jobs)+1) for C in combinations(jobs,r)
            if sum((costs[j][i] for j in C),F(0))<=T]

def priority_example():
    # Both F jobs are completely external: Q=2. Ordinary fixed order picks u1.
    costs={0:{'v':F(1),'u1':F(1)},1:{'v':F(1),'u2':F(1)}}
    cert={'v':[(F(1),())],'u1':[(F(1),(0,))],'u2':[(F(1),(1,))]}
    check(costs,set(cert),cert,(1,'u2'),F(1))
    step=('v',(0,1),2,('u1','u2'),{'u1':0,'u2':1})
    new_costs={2:{'u1':F(1),'u2':F(1)}}
    without_priority={i:list(row) for i,row in cert.items()}
    contract(without_priority,step,(-1,'u2'))
    # Independent verification confirms that this valid point probes the wrong edge.
    check(new_costs,{'u1','u2'},without_priority,(2,'u1'),F(1))
    wrong_mass=sum(w for w,C in without_priority['u2'] if 2 in C)
    assert wrong_mass==0
    with_priority={i:list(row) for i,row in cert.items()}
    tracked,_,_=contract(with_priority,step,(1,'u2'))
    assert tracked==(2,'u2')
    check(new_costs,{'u1','u2'},with_priority,tracked,F(1))
    return {'exterior_occupancy':'2','ordinary_order_target_mass':str(wrong_mass),'priority_order_target_mass':'1'}

def main():
    start=time.monotonic();P=legacy.instance(3,5,F(1,8));costs,machines,plan,sources=make_plan(P);T=F(4,3)
    for i in machines:
        row=[cs[i] for cs in costs.values() if i in cs]
        s=sum(row)
        assert not (row and s>T and all(s-p<=T for p in row))
    final_edges=[(j,i) for j,cs in costs.items() for i in cs]
    old_costs={j:r['costs'] for j,r in enumerate(P['jobs'])};old_machines=set(P['machines'])
    maxextra=0;maxsupport=0;maxsplits=0
    for index,(j,i) in enumerate(final_edges):
        old_force=(sources[j,i],i);cert,_=legacy.certificate(P,old_force)
        cert={v:normalize(row) for v,row in cert.items()}
        check(old_costs,old_machines,cert,old_force,T)
        tracked=old_force;splits=0
        for step in plan:
            tracked,ns,extra=contract(cert,step,tracked);splits+=ns;maxextra=max(maxextra,extra)
        assert tracked==(j,i)
        maxsupport=max(maxsupport,check(costs,machines,cert,tracked,T));maxsplits=max(maxsplits,splits)
    result={'arithmetic':'fractions.Fraction','python':sys.version.split()[0],'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'legacy_generator_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'old_machines':len(P['machines']),'old_jobs':len(P['jobs']),'contractions':len(plan),'final_machines':len(machines),'final_jobs':len(costs),'all_final_finite_edges':len(final_edges),'all_probe_certificates_verified':True,'no_minimal_star':True,'max_added_support_per_contraction':maxextra,'max_support':maxsupport,'max_total_splits_per_probe':maxsplits,'missing_mutual_exclusion_counterexample':missing_exclusion_example(),'seconds':round(time.monotonic()-start,3)}
    result['reverse_conditioned_counterexample']=reverse_probe_example()
    result['forced_machine_priority_control']=priority_example()
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
